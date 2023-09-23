from django.urls import path
from .views import HomeView, VacancyListView, ResumeListView, ResumeAddView, ResumeDetailView, FeedBackView, \
    ResumeUpdateView, ResumeToArchive, ResumeToActive, ResumeDeleteView, VacancyAddView, VacancyDetailView, \
    VacancyUpdateView, VacancyDeleteView, VacancyToArchive, VacancyToActive, AddFollower, \
    ResponsesListView, VacanciesView, ResumeALLView, CategoryListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('feedback/', FeedBackView.as_view(), name='feedback'),
    path('all-vacancies/', VacanciesView.as_view(), name='all_vacancies'),
    path('all-resume/', ResumeALLView.as_view(), name='all_resume'),
    path('all-categories/', CategoryListView.as_view(), name='all_categories'),

    path('vacancies-my-list/', VacancyListView.as_view(), name='vacancies_list'),
    path('vacancies-add/', VacancyAddView.as_view(), name='vacancies_add'),
    path('vacancies-detail/<int:pk>', VacancyDetailView.as_view(), name='vacancies_detail'),
    path('vacancies-detail/<int:pk>/add', AddFollower.as_view(), name='add_follower'),
    path('vacancies-update/<int:pk>', VacancyUpdateView.as_view(), name='vacancies_update'),
    path('vacancies-to-archive/<int:pk>', VacancyToArchive.as_view(), name='vacancies_to_archive'),
    path('vacancies-to-active/<int:pk>', VacancyToActive.as_view(), name='vacancies_to_active'),
    path('vacancies-delete/<int:pk>', VacancyDeleteView.as_view(), name='vacancies_delete'),

    path('responses/', ResponsesListView.as_view(), name='responses'),

    path('resume-my-list/', ResumeListView.as_view(), name='resume_list'),
    path('resume-add', ResumeAddView.as_view(), name='resume_add'),
    path('resume-detail/<int:pk>', ResumeDetailView.as_view(), name='resume_detail'),
    path('resume-update/<int:pk>', ResumeUpdateView.as_view(), name='resume_update'),
    path('resume-to-archive/<int:pk>', ResumeToArchive.as_view(), name='resume_to_archive'),
    path('resume-to-active/<int:pk>', ResumeToActive.as_view(), name='resume_to_active'),
    path('resume-delete/<int:pk>', ResumeDeleteView.as_view(), name='resume_delete'),
]
