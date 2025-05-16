from django.shortcuts import render
from django.http import JsonResponse
from teachers.forms import TeacherForm
from teachers.models import Teacher
from django.db.models import Count, F, Q


# Create your views here.
def index(request):
    name = request.session.get('name', 'Usuário')
    return render(request, 'teachers/index.html', {'person_form': TeacherForm(), 'name': name})


def get_teachers(request):
    ma = request.GET.get('ma')
    if ma:
        try:
            # busca já juntando os relacionamentos
            teacher = (
                Teacher.objects
                .select_related('course__campus__university')
                .get(ma=ma)
            )
            course = teacher.course
            campus = course.campus
            university = campus.university

            data = {
                'person': {
                    'ra': teacher.ma,
                    'name': teacher.name,
                },
                'university': {
                    'acronym': university.acronym,
                    'name': getattr(university, 'name', None)
                },
                'campus': {
                    'id': campus.id,
                    'name': getattr(campus, 'name', None)
                },
                'course': {
                    'id': course.id,
                    'name': getattr(course, 'name', None)
                }
            }
            return JsonResponse({'success': True, 'data': data})
        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Professor não encontrado.'})

    # branch sem 'ma': lista geral com contagem de atributos
    teachers = (
        Teacher.objects
        .annotate(
            num_orientacoes=Count('tccwork', distinct=True),
            num_coorientacoes=Count('tccwork_teacher_cosupervisor_ma_set', distinct=True),
            num_bancas_fm1=Count('tcccommittee', distinct=True),
            num_bancas_fm2=Count('tcccommittee_full_member_2_ma_set', distinct=True),
            num_bancas_am=Count('tcccommittee_alternate_member_ma_set', distinct=True),
            course_name=F('course__name'),
        )
        .annotate(
            num_bancas=F('num_bancas_fm1') + F('num_bancas_fm2') + F('num_bancas_am')
        )
        .values('ma', 'name', 'course_name', 'num_orientacoes', 'num_coorientacoes', 'num_bancas')
    )

    return JsonResponse({'success': True, 'data': list(teachers)})


def register_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            student = form.save()
            return JsonResponse({'success': True, 'message': 'Professor registrado com sucesso!', 'id': student.ma})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def edit_teacher(request, ma):
    try:
        teacher = (Teacher.objects.annotate(
            num_orientacoes=Count('tccwork', distinct=True),
            num_coorientacoes=Count('tccwork_teacher_cosupervisor_ma_set', distinct=True),
            num_bancas_fm1=Count('tcccommittee', distinct=True),
            num_bancas_fm2=Count('tcccommittee_full_member_2_ma_set', distinct=True),
            num_bancas_am=Count('tcccommittee_alternate_member_ma_set', distinct=True))
            .annotate(
                tcc_count=F('num_bancas_fm1') + F('num_bancas_fm2') + F('num_bancas_am') + F('num_bancas_am') + F('num_orientacoes') + F('num_coorientacoes')
            )
                   .get(ma=ma))
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Professor não encontrado.'}, status=400)

    has_tcc = teacher.tcc_count > 0

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if has_tcc:
            new_course_id = form.data.get('course')
            if str(teacher.course_id) != new_course_id:
                form.add_error(
                    'course',
                    'Não é possível mudar de curso pois este professor já tem TCC cadastrado.'
                )

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Professor atualizado com sucesso.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def delete_teacher(request, ma):
    if ma == request.session.get('ma'):
        return JsonResponse({'success': False, 'message': 'Não é possível remover a si mesmo.'})

    try:
        teacher = (Teacher.objects.annotate(
            num_orientacoes=Count('tccwork', distinct=True),
            num_coorientacoes=Count('tccwork_teacher_cosupervisor_ma_set', distinct=True),
            num_bancas_fm1=Count('tcccommittee', distinct=True),
            num_bancas_fm2=Count('tcccommittee_full_member_2_ma_set', distinct=True),
            num_bancas_am=Count('tcccommittee_alternate_member_ma_set', distinct=True))
                   .annotate(
            tcc_count=F('num_bancas_fm1') + F('num_bancas_fm2') + F('num_bancas_am') + F('num_bancas_am') + F(
                'num_orientacoes') + F('num_coorientacoes')
        )
                   .get(ma=ma))
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Professor não encontrado.'}, status=400)

    if teacher.tcc_count > 0:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível excluir este professor pois ele já possui TCC cadastrado.'
        }, status=400)

    teacher.delete()
    return JsonResponse({'success': True, 'message': 'Professor excluído com sucesso.'})