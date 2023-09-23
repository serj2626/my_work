from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import User, Account
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView

from users.forms import SignUPForm, LoginForm, AccountForm


class SignUPView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUPForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрированы!'
    title = 'Регистрация'


class AuthenticationView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    title = 'Авторизация'
    success_message = 'Вы вошли на сайт'


class AccountView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Account
    template_name = 'users/account.html'


class AccountUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'users/account_update.html'
    success_message = 'Данные успешно обновлены!'

    # success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('users:account', kwargs={"slug": self.kwargs['slug']})


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'users/favorites.html'