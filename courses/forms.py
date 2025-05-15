from django import forms
from courses.models import Course

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