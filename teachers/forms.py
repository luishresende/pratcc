from django import forms
from core.forms import PersonForm
from teachers.models import Teacher


class TeacherForm(PersonForm):
    class Meta:
        model = Teacher
        fields = ['ma', 'name', 'course']
        labels = {
            'ma': 'Número de mátricula*',
            'name': 'Nome*',
            'university': 'Universidade*',
            'campus': 'Campus*',
            'course': 'Curso*',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ma': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'course': forms.Select(attrs={'class': 'form-select', 'id': 'course_select', 'required': True}),
        }