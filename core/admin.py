from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Resume, Vacancy, Category, Experience, FeedBack, PersonFavorites, CompanyFavorites


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'status_resume')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('company', 'category', 'job_title', 'slug', 'status_vacancy')


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('title', 'slug')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    ist_display = ('user', 'job_title', 'name_company')


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    ist_display = ('name', 'email')


@admin.register(PersonFavorites)
class PersonFavoritesAdmin(admin.ModelAdmin):
    ist_display = ('user', 'vacancy')


@admin.register(CompanyFavorites)
class CompanyFavoritesAdmin(admin.ModelAdmin):
    ist_display = ('user', 'resume')
