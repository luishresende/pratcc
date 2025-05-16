from core.forms import PersonForm
from teachers.models import Teacher
import re
from django import forms
from django.core.exceptions import ValidationError


class TeacherForm(PersonForm):
    class Meta:
        model = Teacher
        fields = ['ma', 'name', 'course']
        labels = {
            'ma': 'Número de matrícula*',
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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[A-Za-zÀ-ÿ\s\-]+$', name):
            raise ValidationError('O nome deve conter apenas letras, espaços e hífens.')
        return name

    def clean_ma(self):
        ma = self.cleaned_data.get('ma')
        if not ma:
            raise ValidationError('A matrícula é obrigatório.')
        if len(ma) != 8:
            raise ValidationError('O matrícula deve ter exatamente 8 caracteres.')
        if not re.match(r'^[A-Za-z][0-9]{7}$', ma):
            raise ValidationError('O matrícula deve começar com uma letra seguida de 7 números.')
        return ma