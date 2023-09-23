from django.contrib import admin
from .models import User, Account


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'data_client', 'country', 'slug')
