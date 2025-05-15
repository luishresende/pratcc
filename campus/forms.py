from django import forms
from campus.models import Campus
from universities.models import University
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