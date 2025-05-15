from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, F

from students.forms import StudentForm
from students.models import Student


# Create your views here.
def index(request):
    return render(request, 'students/index.html', {'person_form': StudentForm()})


def get_students(request):
    ra = request.GET.get('ra')
    if ra:
        try:
            # busca já juntando os relacionamentos
            student = (
                Student.objects
                       .select_related('course__campus__university')
                       .get(ra=ra)
            )
            course     = student.course
            campus     = course.campus
            university = campus.university

            data = {
                'person': {
                    'ra': student.ra,
                    'name': student.name,
                },
                'university': {
                    'acronym':   university.acronym,
                    'name': getattr(university, 'name', None)
                },
                'campus': {
                    'id':   campus.id,
                    'name': getattr(campus, 'name', None)
                },
                'course': {
                    'id':   course.id,
                    'name': getattr(course, 'name', None)
                }
            }
            return JsonResponse({'success': True, 'data': data})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Estudante não encontrado.'})

    # branch sem 'ra': lista geral com contagem de TCCs
    students = (
        Student.objects
        .annotate(tcc_count=Count('tccworks'), course_name=F('course__name'))
        .values('name', 'ra', 'tcc_count', 'course_name')
    )

    return JsonResponse({'success': True, 'data': list(students)})


def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return JsonResponse({'success': True, 'message': 'Aluno registrado com sucesso!', 'id': student.ra})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def edit_student(request, ra):
    try:
        student = Student.objects.annotate(tcc_count=Count('tccworks')).get(ra=ra)
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Aluno não encontrado.'}, status=400)

    has_tcc = student.tcc_count > 0

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if has_tcc:
            new_course_id = form.data.get('course')
            if str(student.course_id) != new_course_id:
                form.add_error(
                    'course',
                    'Não é possível mudar de curso pois este aluno já tem TCC cadastrado.'
                )

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Aluno atualizado com sucesso.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def delete_student(request, ra):
    try:
        student = Student.objects.annotate(tcc_count=Count('tccworks')).get(ra=ra)
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Aluno não encontrado.'}, status=400)

    if student.tcc_count > 0:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível excluir este aluno pois ele já possui TCC cadastrado.'
        }, status=400)

    student.delete()
    return JsonResponse({'success': True, 'message': 'Aluno excluído com sucesso.'})