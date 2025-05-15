from django.http import JsonResponse
from universities.models import University
from campus.models import Campus
from universities.forms import UniversityForm
from django.shortcuts import render
from django.views.decorators.http import require_GET


# Create your views here.
def university_register(request):
 if request.method == 'POST':
  form = UniversityForm(request.POST)
  if form.is_valid():
   acronym = form.cleaned_data['acronym']
   if University.objects.filter(acronym=acronym).exists():
    form.add_error('acronym', 'Uma universidade com essa sigla já existe.')
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

   form.save()
   return JsonResponse({'success': True, 'message': 'Universidade registrada com sucesso!'})
  else:
   return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def edit_university(request, acronym):
    try:
        university = University.objects.get(acronym=acronym)
    except University.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Universidade não encontrada.'}, status=404)

    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            # A sigla (acronym) não pode ser alterada, então não é necessário fazer nenhuma validação adicional para ela.
            form.save()
            return JsonResponse({'success': True, 'message': 'Universidade editada com sucesso!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = UniversityForm(instance=university)

    return render(request, 'courses/index.html', {'form': form})


@require_GET
def get_university_by_acronym(request):
    acronym = request.GET.get('acronym')

    if not acronym:
        return JsonResponse({'success': False, 'message': 'A sigla não foi fornecida.'}, status=400)

    try:
        university = University.objects.get(acronym=acronym)
        data = {
            'acronym': university.acronym,
            'name': university.name,
        }
        return JsonResponse({'success': True, 'university': data})
    except University.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Universidade não encontrada.'}, status=404)


def delete_university(request, acronym):
    try:
        university = University.objects.get(acronym=acronym)
        campus = Campus.objects.filter(university=university)
        if campus.exists():
            print('campus existe')
            return JsonResponse({'success': False, 'message': 'Não é possível remover uma universidade com campus registrado.'}, status=404)

    except University.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Universidade não encontrada.'}, status=404)

    # Remover o objeto
    university.delete()

    # Retornar uma resposta JSON indicando sucesso
    return JsonResponse({'success': True, 'message': 'Universidade removida com sucesso!'})