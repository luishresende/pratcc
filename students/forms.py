import re
from django import forms
from core.forms import PersonForm
from django.core.exceptions import ValidationError
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

    def clean_ra(self):
        ra = self.cleaned_data.get('ra')
        if not ra:
            raise ValidationError('O RA é obrigatório.')
        if len(ra) != 8:
            raise ValidationError('O RA deve ter exatamente 8 caracteres.')
        if not re.match(r'^[A-Za-z][0-9]{7}$', ra):
            raise ValidationError('O RA deve começar com uma letra seguida de 7 números.')
        return ra

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[A-Za-zÀ-ÿ\s\-]+$', name):
            raise ValidationError('O nome deve conter apenas letras, espaços e hífens.')
        return name