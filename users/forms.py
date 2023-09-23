from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django_countries.fields import CountryField

from .models import User, TYPE_USER, Account


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='телефон', widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите телефон'}))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUPForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите телефон'}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    type = forms.CharField(label='', widget=forms.RadioSelect(choices=TYPE_USER))
    password1 = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('type', 'username', 'email', 'password1', 'password2')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('fullname', 'data_client', 'country', 'image')

    # def clean(self):
    #
    #     if self.instance.user.type == 'person':
    #         self.instance.fullname = forms.CharField(label='Имя и фамилия')
    #         self.instance.data_client = forms.IntegerField(label='Возраст')
    #     else:
    #         self.instance.fullname = forms.CharField(label='Название компании')
    #         self.instance.data_client = forms.CharField(label='ИНН')
    #     return self.instance
