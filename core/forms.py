from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Resume, Vacancy, FeedBack


class ResumeAddForm(forms.ModelForm):
    image = forms.ImageField(label='Аватар')

    class Meta:
        model = Resume
        exclude = ('user', 'date', 'responses', 'experience')
        widgets = {

            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5", 'placeholder': 'Введите информацию о себе'},
                config_name="extends"),
            "skills": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5", 'placeholder': 'Введите свои навыки'},
                config_name="extends")}


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = '__all__'


class VacancyAddForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ('company', 'date', 'responses', 'slug', 'followers')
        widgets = {

            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5", 'placeholder': 'Введите описание вакансии'},
                config_name="extends"),
            "charge": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5", 'placeholder': 'Введите обязанности вакансии'},
                config_name="extends"),
            "conditions": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5", 'placeholder': 'Введите условия вакансии'},
                config_name="extends")
        }
