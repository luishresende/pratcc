from importlib.metadata import requires

from django import forms
from core.forms import PersonForm
from students.models import Student


class StudentForm(PersonForm):
    class Meta:
        model = Student
        fields = ['ra', 'name', 'course']
        labels = {
            'ra': 'Registro Acadêmico*',
            'name': 'Nome*',
            'university': 'Universidade*',
            'campus': 'Campus*',
            'course': 'Curso*',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ra': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'course': forms.Select(attrs={'class': 'form-select', 'id': 'course_select', 'required': True}),
        }