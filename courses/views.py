from django.shortcuts import render
from django.http import JsonResponse

from courses.models import Course
from students.models import Student
from teachers.models import Teacher
from universities.forms import UniversityForm
from universities.models import University
from campus.forms import CampusForm
from campus.models import Campus
from courses.forms import CourseForm
import json


# Create your views here.
def index(request):
    universities = University.objects.values('name', 'acronym')
    universities_list = list(universities)

    return render(request,
                  'courses/index.html',
                  {'university_form': UniversityForm(), 'universities': json.dumps(universities_list),
                   'campus_form': CampusForm(), 'course_form': CourseForm()})


def course_register(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return JsonResponse({'success': True, 'message': 'Curso registrado com sucesso!', 'id': course.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=400)


def get_courses(request):
    campus_id = request.GET.get('campus_id')
    course_id = request.GET.get('course_id')

    # Verifica se ambos os parâmetros estão ausentes
    if not campus_id and not course_id:
        return JsonResponse({'error': 'Nenhum identificador de campus ou curso informado'}, status=400)

    if course_id:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Curso não encontrado'}, status=404)

        # Obtendo o campus relacionado ao curso
        campus = course.campus

        # Acessando o acrônimo da universidade associada ao campus
        university_acronym = campus.university.acronym if campus.university else None

        # Retornando informações do campus e curso
        return JsonResponse({
            'success': True,
            'data': {
                'id': course.id,
                'name': course.name,
                'campus_name': campus.name,
                'university': university_acronym,
                'campus_id' : campus.id,
            }
        })

    if campus_id:
        try:
            campus = Campus.objects.get(id=campus_id)
        except Campus.DoesNotExist:
            return JsonResponse({'error': 'Campus não encontrado'}, status=404)

        courses = Course.objects.filter(campus=campus).values('id', 'name')

        return JsonResponse({'success': True, 'data': list(courses)})

def edit_course(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Curso não encontrada.'}, status=404)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Curso editado com sucesso!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/index.html', {'form': form})

def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
        students = Student.objects.filter(course=course)
        teachers = Teacher.objects.filter(course=course)

        if students.exists() or teachers.exists():
            return JsonResponse({'success': False, 'message': 'Não é possível remover um curso com professores ou alunos registrados nele.'}, status=400)
    except Course.DoesNotExist:
        return JsonResponse({'sucess': False, 'message': 'Curso não encontrado.'}, status=404)

    course.delete()

    return JsonResponse({'success': True, 'message': 'Curso removido com sucesso!'})