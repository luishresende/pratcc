# forms.py
from django import forms
from universities.models import University


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['acronym', 'name']
        labels = {
            'acronym': 'Sigla*',
            'name': 'Nome*',
        }
        widgets = {
            'acronym': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sigla',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da universidade',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Se for edição, desabilita o campo acronym
            self.fields['acronym'].disabled = True


