from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from tccs.forms import TccWorkForm, TccCommitteeForm, TccDocumentsForm
from tccs.models import TccCommittee, TccDocuments, TccWork
from teachers.models import Teacher


# Create your views here.
def index(request):
    name = request.session.get('name', 'Usuário')
    return render(request, 'tccs/index.html',
                  {'tcc_work_form': TccWorkForm(),
                   'tcc_committe_form': TccCommitteeForm(),
                   'tcc_documents_form': TccDocumentsForm(),
                   'name': name})


def register_tcc_work(request):
    if request.method == 'POST':
        form = TccWorkForm(request.POST)

        if form.is_valid():
            advisor = form.cleaned_data['teacher_advisor_ma']
            cosupervisor = form.cleaned_data.get('teacher_cosupervisor_ma')
            student = form.cleaned_data['student_ra']
            year = form.cleaned_data['year']
            semester = form.cleaned_data['semester']

            errors = {}

            # Valida se orientador existe
            if not Teacher.objects.filter(pk=advisor.pk).exists():
                errors['teacher_advisor_ma'] = 'Orientador não encontrado.'

            # Valida coorientador
            if cosupervisor:
                if not Teacher.objects.filter(pk=cosupervisor.pk).exists():
                    errors['teacher_cosupervisor_ma'] = 'Coorientador não encontrado.'
                elif advisor.pk == cosupervisor.pk:
                    errors['teacher_cosupervisor_ma'] = 'Coorientador não pode ser o mesmo que o orientador.'

            # Validação uniqueness: aluno não pode ter 2 TCCs no mesmo ano e semestre
            existing = TccWork.objects.filter(student_ra=student, year=year, semester=semester)
            if form.instance.pk:
                existing = existing.exclude(pk=form.instance.pk)
            if existing.exists():
                errors['student_ra'] = 'Este aluno já possui um TCC registrado para este ano e semestre.'

            if errors:
                return JsonResponse({'success': False, 'errors': errors})

            instance = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Trabalho de TCC cadastrado com sucesso!',
                'id': instance.tcc_id
            })

        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Método não permitido. Use POST.'}, status=405)


def edit_tcc_work(request, tcc_id):
    if request.method == 'POST':
        try:
            tcc_instance = TccWork.objects.get(pk=tcc_id)
        except TccWork.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'TCC não existente.'}, status=404)
        form = TccWorkForm(request.POST, instance=tcc_instance)

        if form.is_valid():
            student = form.cleaned_data['student_ra']
            year = form.cleaned_data['year']
            semester = form.cleaned_data['semester']

            errors = {}

            if errors:
                return JsonResponse({'success': False, 'errors': errors})

            instance = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Trabalho de TCC atualizado com sucesso!',
                'id': instance.tcc_id
            })

        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Método não permitido. Use POST.'}, status=405)


def get_tcc_work(request):
    tcc_id = request.GET.get('tcc_id')

    if tcc_id:
        try:
            tcc = TccWork.objects.select_related(
                'student_ra', 'teacher_advisor_ma', 'teacher_cosupervisor_ma'
            ).get(pk=tcc_id)

            # Comissão
            comitte_data = None
            tcc_committe = TccCommittee.objects.select_related(
                'full_member_1_ma',
                'full_member_2_ma',
                'alternate_member_ma'
            ).filter(tccw=tcc).first()

            if tcc_committe:
                comitte_data = {
                    'full_member_1': {
                        'ma': tcc_committe.full_member_1_ma.ma,
                        'name': tcc_committe.full_member_1_ma.name
                    },
                    'full_member_2': {
                        'ma': tcc_committe.full_member_2_ma.ma,
                        'name': tcc_committe.full_member_2_ma.name
                    },
                    'alternate_member': {
                        'ma': tcc_committe.alternate_member_ma.ma,
                        'name': tcc_committe.alternate_member_ma.name
                    },
                    'defense_date': tcc_committe.defense_date.strftime('%Y-%m-%d'),
                    'defense_location': tcc_committe.defense_location,
                    'autorization_letter': tcc_committe.authorization_letter_submitted
                }

            # Documentos
            tcc_documents_data = None
            try:
                tcc_documents = TccDocuments.objects.get(tccw=tcc)
                tcc_documents_data = {
                    'fm1_evaluation_form': bool(tcc_documents.fm1_evaluation_form),
                    'fm2_evaluation_form': bool(tcc_documents.fm2_evaluation_form),
                    'fm3_evaluation_form': bool(tcc_documents.fm3_evaluation_form),
                    'approvation_term': bool(tcc_documents.approvation_term),
                    'end_monograph': bool(tcc_documents.end_monograph),
                    'end_monograph_in_lib': bool(tcc_documents.end_monograph_in_lib),
                    'recorded_data': bool(tcc_documents.recorded_data),
                }
            except TccDocuments.DoesNotExist:
                tcc_documents_data = None
                pass

            data = {
                'tcc_work': {
                    'tcc_id': tcc_id,
                    'title': tcc.title,
                    'year': tcc.year,
                    'semester': tcc.semester,
                    'tcc_num': tcc.tcc_num,
                    'student_ra': tcc.student_ra.ra,
                },
                'advisor': {
                    'ma': tcc.teacher_advisor_ma.ma,
                },
                'cosupervisor': {
                    'ma': tcc.teacher_cosupervisor_ma.ma if tcc.teacher_cosupervisor_ma else None,
                },
                'committe': comitte_data,
                'documents': tcc_documents_data
            }

            return JsonResponse({'success': True, 'data': data})
        except TccWork.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'TCC não encontrado'}, status=404)
    else:
        tccs = TccWork.objects.annotate(
            student_name=F('student_ra__name'),
            advisor_name=F('teacher_advisor_ma__name'),
        ).values('tcc_id', 'student_name', 'title', 'advisor_name', 'tcc_num')

        return JsonResponse({'success': True, 'data': list(tccs)})


def delete_tcc_work(request, tcc_id):
    if request.method == 'POST':
        try:
            tcc_work = TccWork.objects.get(pk=tcc_id)
        except TccWork.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'TCC não encontrado'}, status=404)

        tcc_documents = TccDocuments.objects.filter(pk=tcc_work).first()
        if tcc_documents:
            return JsonResponse({'success': False, 'message': 'Não é possível deletar um TCC já defendido.'})

        tcc_committee = TccCommittee.objects.filter(pk=tcc_work).first()

        if tcc_committee:
            tcc_committee.delete()

        tcc_work.delete()
        return JsonResponse({'success': True, 'message': 'TCC deletado com sucesso!'})


def register_tcc_committe(request):
    if request.method == 'POST':
        form = TccCommitteeForm(request.POST)

        if form.is_valid():
            tcc_work = form.cleaned_data['tccw']
            full_member_1_ma = form.cleaned_data['full_member_1_ma']
            full_member_2_ma = form.cleaned_data['full_member_2_ma']
            alternate_member_ma = form.cleaned_data['alternate_member_ma']
            defense_location = form.cleaned_data['defense_location']
            defense_date = form.cleaned_data['defense_date']

            teacher_advisor = tcc_work.teacher_advisor_ma
            teacher_cosupervisor = tcc_work.teacher_cosupervisor_ma

            errors = {}

            if not Teacher.objects.filter(pk=full_member_1_ma.pk).exists():
                errors['full_member_1_ma'] = 'Professor 1 não encontrado'

            if not Teacher.objects.filter(pk=full_member_2_ma.pk).exists():
                errors['full_member_2_ma'] = 'Professor 2 não encontrado'

            if not Teacher.objects.filter(pk=alternate_member_ma.pk).exists():
                errors['alternate_member_ma'] = 'Professor suplente não encontrado'

            if errors:
                return JsonResponse({'success': False, 'errors': errors})

            values = [
                teacher_advisor.ma if teacher_advisor else None,
                teacher_cosupervisor.ma if teacher_cosupervisor else None,
                full_member_1_ma.ma if full_member_1_ma else None,
                full_member_2_ma.ma if full_member_2_ma else None,
                alternate_member_ma.ma if alternate_member_ma else None,
            ]
            values = [v for v in values if v is not None]
            has_duplicates = len(values) != len(set(values))

            if len(values) != len(set(values)):
                return JsonResponse({'success': False, 'message': 'Um professor pode ter apenas um papel em um TCC.'})

            instance = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Trabalho de TCC cadastrado com sucesso!',
                'id': instance.tccw.tcc_id
            })

        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Método não permitido. Use POST.'}, status=405)


def edit_tcc_committe(request, committe_id):
    if request.method == 'POST':
        try:
            committee_instance = TccCommittee.objects.get(pk=committe_id)
        except TccCommittee.DoesNotExist:
            return JsonResponse({'success': False, 'message': "Banca de TCC não registrada"}, status=404)
        form = TccCommitteeForm(request.POST, instance=committee_instance)

        if form.is_valid():
            tcc_work = form.cleaned_data['tccw']
            full_member_1_ma = form.cleaned_data['full_member_1_ma']
            full_member_2_ma = form.cleaned_data['full_member_2_ma']
            alternate_member_ma = form.cleaned_data['alternate_member_ma']

            teacher_advisor = tcc_work.teacher_advisor_ma
            teacher_cosupervisor = tcc_work.teacher_cosupervisor_ma

            errors = {}

            if not Teacher.objects.filter(pk=full_member_1_ma.pk).exists():
                errors['full_member_1_ma'] = 'Professor 1 não encontrado'

            if not Teacher.objects.filter(pk=full_member_2_ma.pk).exists():
                errors['full_member_2_ma'] = 'Professor 2 não encontrado'

            if not Teacher.objects.filter(pk=alternate_member_ma.pk).exists():
                errors['alternate_member_ma'] = 'Professor suplente não encontrado'

            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)

            values = [
                teacher_advisor.ma if teacher_advisor else None,
                teacher_cosupervisor.ma if teacher_cosupervisor else None,
                full_member_1_ma.ma if full_member_1_ma else None,
                full_member_2_ma.ma if full_member_2_ma else None,
                alternate_member_ma.ma if alternate_member_ma else None,
            ]
            values = [v for v in values if v is not None]

            if len(values) != len(set(values)):
                return JsonResponse({'success': False, 'message': 'Um professor pode ter apenas um papel em um TCC.'}, status=400)

            instance = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Comitê de TCC atualizado com sucesso!',
                'id': instance.tccw.tcc_id
            })

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Método não permitido. Use POST.'}, status=405)


def register_tcc_documents(request, tcc_id):
    if request.method == 'POST':
        try:
            tcc_work = TccWork.objects.get(pk=tcc_id)
        except TccWork.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'TCC não encontrado'}, status=404)

        try:
            tcc_committee = TccCommittee.objects.get(tccw=tcc_work)
        except TccCommittee.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Carta de autorização ainda não foi entregue'})

        try:
            tcc_documents = TccDocuments.objects.get(tccw=tcc_work)
            return JsonResponse({'success': False, 'message': 'Defesa de TCC já registrada!'}, status=404)
        except TccDocuments.DoesNotExist:
            pass

        TccDocuments.objects.create(tccw=tcc_work)

        return JsonResponse({'success': True, 'message': 'Defesa registrada com sucesso!'})


def edit_tcc_documents(request, tcc_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

    try:
        tcc_work = TccWork.objects.get(pk=tcc_id)
    except TccWork.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'TCC não encontrado'}, status=404)

    try:
        tcc_documents = TccDocuments.objects.get(tccw=tcc_work)
    except TccDocuments.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Documentos ainda não registrados'}, status=404)

    # Fazemos a verificação campo por campo
    data = request.POST
    updated = False
    for field in TccDocumentsForm.Meta.fields:
        if field in data:
            new_value = data.get(field) in ['1', 'true', 'True', 'on']
            current_value = getattr(tcc_documents, field)

            # Só atualiza se estava como 0 e o novo valor for True
            if current_value == 0 and new_value:
                setattr(tcc_documents, field, 1)
                updated = True

            # Impede desmarcar valores já marcados
            elif current_value == 1 and not new_value:
                return JsonResponse({
                    'success': False,
                    'message': f'O campo "{field}" já está marcado e não pode ser desmarcado.'
                }, status=400)

    if updated:
        tcc_documents.save()
        return JsonResponse({'success': True, 'message': 'Documentos atualizados com sucesso!'})
    else:
        return JsonResponse({'success': True, 'message': 'Nenhuma alteração realizada.'})