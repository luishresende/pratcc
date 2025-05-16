from django import forms
from tccs.models import TccWork, TccCommittee, TccDocuments
from teachers.models import Teacher
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


class TccWorkForm(forms.ModelForm):
    SEMESTER_CHOICES = [(1, '1'), (2, '2')]
    TCC_NUM_CHOICES = [(1, '1'), (2, '2')]

    semester = forms.ChoiceField(
        choices=SEMESTER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select required-input', 'required': True}),
        label='Semestre',
        required=True,
    )

    tcc_num = forms.ChoiceField(
        choices=TCC_NUM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select required-input', 'required': True}),
        label='Fase',
        required=True,
    )

    class Meta:
        model = TccWork
        fields = [
            'title', 'year', 'semester', 'tcc_num',
            'student_ra', 'teacher_advisor_ma', 'teacher_cosupervisor_ma'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control required-input', 'required': True}),
            'year': forms.NumberInput(attrs={'class': 'form-control required-input', 'required': True}),
            'student_ra': forms.Select(attrs={'class': 'form-select required-input', 'required': True}),
            'teacher_advisor_ma': forms.Select(attrs={'class': 'form-select required-input', 'required': True}),
            'teacher_cosupervisor_ma': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['teacher_advisor_ma'].queryset = Teacher.objects.filter(course__campus__university__acronym='UTFPR')

        # Torna todos os campos obrigatórios, exceto o coorientador
        self.fields['title'].required = True
        self.fields['year'].required = True
        self.fields['semester'].required = True
        self.fields['tcc_num'].required = True
        self.fields['student_ra'].required = True
        self.fields['teacher_advisor_ma'].required = True
        self.fields['teacher_cosupervisor_ma'].required = False

        # Se for edição, tornar os campos de orientador e coorientador somente leitura
        if self.instance and self.instance.pk:
            self.fields['year'].disabled = True
            self.fields['semester'].disabled = True
            self.fields['tcc_num'].disabled = True
            self.fields['student_ra'].disabled = True
            self.fields['teacher_advisor_ma'].disabled = True
            self.fields['teacher_cosupervisor_ma'].disabled = True

    def clean_semester(self):
        semester = int(self.cleaned_data.get('semester'))
        if semester not in [1, 2]:
            raise ValidationError("O semestre deve ser 1 ou 2.")
        return semester

    def clean_tcc_num(self):
        tcc_num = int(self.cleaned_data.get('tcc_num'))
        if tcc_num not in [1, 2]:
            raise ValidationError("A fase do TCC deve ser 1 ou 2.")
        return tcc_num

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = datetime.now().year
        if year is not None:
            if year <= 2020:
                raise ValidationError("O ano deve ser maior que 2020.")
            if year > current_year:
                raise ValidationError(f"O ano não pode ser maior que o ano atual ({current_year}).")
        return year

    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        semester = cleaned_data.get('semester')

        if year and semester:
            current_year = datetime.now().year
            current_month = datetime.now().month

            # Define semestre atual: 1 para meses jan-jun, 2 para jul-dez
            current_semester = 1 if current_month <= 6 else 2

            if year == current_year:
                # Se for o mesmo ano, semestre escolhido deve ser coerente
                if (semester == '1' and current_semester == 2) or (semester == '2' and current_semester == 1):
                    raise ValidationError(
                        f"Semestre incompatível com o período atual: "
                        f"Estamos no semestre {current_semester} do ano {current_year}."
                    )
        return cleaned_data

class TccCommitteeForm(forms.ModelForm):
    class Meta:
        model = TccCommittee
        fields = [
            'tccw',
            'full_member_1_ma',
            'full_member_2_ma',
            'alternate_member_ma',
            'defense_location',
            'defense_date',
            'authorization_letter_submitted',
        ]
        widgets = {
            'tccw': forms.HiddenInput(attrs={
                'required': True
            }),
            'full_member_1_ma': forms.Select(attrs={
                'class': 'form-control required-input col-md-4',
                'required': True,
            }),
            'full_member_2_ma': forms.Select(attrs={
                'class': 'form-control required-input col-md-4',
                'required': True,
            }),
            'alternate_member_ma': forms.Select(attrs={
                'class': 'form-control required-input col-md-4',
                'required': True,
            }),
            'defense_location': forms.TextInput(attrs={
                'class': 'form-control required-input col-md-6',
                'required': True,
            }),
            'defense_date': forms.DateInput(attrs={
                'class': 'form-control required-input col-md-2',
                'type': 'date',
                'required': True,
            }),
            'authorization_letter_submitted': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra professores da universidade UTFPR
        teachers = Teacher.objects.all()
        utfpr_teachers = Teacher.objects.filter(course__campus__university__acronym='UTFPR')
        self.fields['full_member_1_ma'].queryset = teachers
        self.fields['full_member_2_ma'].queryset = teachers
        self.fields['alternate_member_ma'].queryset = teachers

    def clean_defense_date(self):
        defense_date = self.cleaned_data.get('defense_date')
        if defense_date and defense_date.date() <= timezone.now().date():
            raise ValidationError('A data de defesa deve ser posterior à data atual.')
        return defense_date


class TccDocumentsForm(forms.ModelForm):
    fm1_evaluation_form = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))
    fm2_evaluation_form = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))
    fm3_evaluation_form = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))
    approvation_term = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))
    end_monograph = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))
    end_monograph_in_lib = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))
    recorded_data = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-1'}))

    class Meta:
        model = TccDocuments
        fields = [
            'fm1_evaluation_form',
            'fm2_evaluation_form',
            'fm3_evaluation_form',
            'approvation_term',
            'end_monograph',
            'end_monograph_in_lib',
            'recorded_data',
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Converte bools para int como o modelo espera
        for field in self.fields:
            cleaned_data[field] = int(bool(cleaned_data.get(field)))
        return cleaned_data