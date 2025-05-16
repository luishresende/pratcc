from django import forms
from courses.models import Course
from django.core.exceptions import ValidationError
import re

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['campus', 'name']
        labels = {
            'campus': 'Campus*',
            'name': 'Curso*',
        }
        widgets = {
            'campus': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
                'disabled': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d', name):
            raise ValidationError('O nome do curso não pode conter números.')
        return name