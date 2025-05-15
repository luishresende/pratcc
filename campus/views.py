from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

import campus
from campus.models import City, Campus
from courses.models import Course
from campus.forms import CampusForm
from universities.models import University
# Create your views here.


def get_cities_by_state(request):
    state_acronym = request.GET.get('state_acronym')
    if not state_acronym:
        return JsonResponse({'error': 'Estado não informado'}, status=400)

    cities = City.objects.filter(state_acronym=state_acronym).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


def get_campus(request):
    campus_id = request.GET.get('id')
    university_acronym = request.GET.get('acronym')

    # Verifica se ambos os parâmetros estão ausentes
    if not campus_id and not university_acronym:
        return JsonResponse({'error': 'Nenhum identificador de universidade ou campus informado'}, status=400)

    if campus_id:
        try:
            campus = Campus.objects.select_related('city__state_acronym').get(id=campus_id)
        except Campus.DoesNotExist:
            return JsonResponse({'error': 'Campus não encontrado'}, status=404)

        campus_data = {
            'id': campus.id,
            'name': campus.name,
            'university': campus.university.acronym,
            'city': campus.city.id,
            'state': campus.city.state_acronym.acronym,
        }
        return JsonResponse({'success': True, 'data': campus_data})

    if university_acronym:
        # Buscar campus pela sigla da universidade
        try:
            university = University.objects.get(acronym=university_acronym)
        except University.DoesNotExist:
            return JsonResponse({'error': 'Universidade não cadastrada'}, status=400)

        campuses = Campus.objects.filter(university=university) \
            .annotate(course_count=Count('course')) \
            .values('id', 'name', 'course_count')

        return JsonResponse({'success': True, 'data': list(campuses)}, safe=False)


def campus_register(request):
    if request.method == 'POST':
        form = CampusForm(request.POST)
        if form.is_valid():
            campus = form.save()
            return JsonResponse({'success': True, 'message': 'Campus registrado com sucesso!', 'id': campus.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def edit_campus(request, id):
    try:
        campus = Campus.objects.get(id=id)
    except Campus.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Campus não encontrada.'}, status=404)

    if request.method == 'POST':
        form = CampusForm(request.POST, instance=campus)
        if form.is_valid():
            # A sigla (acronym) não pode ser alterada, então não é necessário fazer nenhuma validação adicional para ela.
            form.save()
            return JsonResponse({'success': True, 'message': 'Campus editado com sucesso!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = CampusForm(instance=campus)

    return render(request, 'courses/index.html', {'form': form})


def delete_campus(request, id):
    try:
        campus = Campus.objects.get(id=id)
        courses = Course.objects.filter(campus=campus)
        if courses.exists():
            return JsonResponse({'success': False, 'message': 'Não é possível remover um campus com curso(s) registrado(s).'}, status=400)

    except University.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Campus não encontrado.'}, status=400)

    # Remover o objeto
    campus.delete()

    # Retornar uma resposta JSON indicando sucesso
    return JsonResponse({'success': True, 'message': 'Campus removido com sucesso!'})