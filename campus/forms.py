from django import forms
from campus.models import Campus
import re
from django.core.exceptions import ValidationError
from campus.models import City, State  # supondo que estão em outro app


class CampusForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        label="Estado*",
        widget=forms.Select(attrs={'class': 'form-select', 'required': True})
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # Inicialmente sem opções
        label="Cidade*",
        widget=forms.Select(attrs={'class': 'form-select', 'required': True})
    )

    class Meta:
        model = Campus
        fields = ['university', 'state', 'city', 'name']
        labels = {
            'name': 'Nome*',
            'university': 'Universidade*',
            'state': 'Estado*',
            'city': 'Cidade*',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'readonly': True}),
            'state': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'city': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Preenche o queryset de estados
        self.fields['state'].queryset = State.objects.all()

        if 'state' in self.data:
            try:
                state_acronym = self.data.get('state')
                self.fields['city'].queryset = City.objects.filter(state_acronym=state_acronym).order_by('name')
            except (ValueError, TypeError):
                self.fields['city'].queryset = City.objects.none()
        elif self.instance.pk and self.instance.city:
            self.fields['city'].queryset = City.objects.filter(state_acronym=self.instance.city.state_acronym).order_by(
                'name')

        # Desabilita a universidade se for edição
        if self.instance and self.instance.pk:
            self.fields['university'].disabled = True

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('O nome do campus é obrigatório.')
        if re.search(r'\d', name):
            raise ValidationError('O nome do campus não deve conter números.')
        return name
