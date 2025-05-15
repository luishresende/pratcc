from django import forms
from courses.models import Course
from campus.models import Campus
from universities.models import University


class PersonForm(forms.ModelForm):
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'university_select'}),
        label="Universidade"
    )
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'campus_select'}),
        label="Campus"
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'course_select'}),
        label="Curso"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uni_id = self.data.get('university') or getattr(self.instance, 'university_id', None)
        if uni_id:
            self.fields['campus'].queryset = Campus.objects.filter(university_id=uni_id).order_by('name')
        else:
            self.fields['campus'].queryset = Campus.objects.none()

        camp_id = self.data.get('campus') or getattr(self.instance, 'campus_id', None)
        if camp_id:
            self.fields['course'].queryset = Course.objects.filter(campus_id=camp_id).order_by('name')
        else:
            self.fields['course'].queryset = Course.objects.none()