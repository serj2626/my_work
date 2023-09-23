from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, UpdateView, ListView

from core.forms import ResumeAddForm, FeedBackForm, VacancyAddForm
from core.models import Resume, Vacancy, Category


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "core/category_list.html"


class FeedBackView(View):

    def post(self, request):
        feedback = FeedBackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
            messages.info(request, 'Ваш запрос успешно отправлен!')
            return redirect('home')
        messages.warning(request, 'Ваш запрос введен некорректно !')
        return render(request, 'core/feedback.html')

    def get(self, request):
        return render(request, 'core/feedback.html')


################################################   Resume   ############################################################

class ResumeALLView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'core/resume-all.html'
    context_object_name = 'all_resume'


class ResumeListView(View):
    def get(self, request):
        all_resume = Resume.objects.filter(user=request.user)
        return render(request, 'core/resume-list.html', {'all_resume': all_resume})


class ResumeAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeAddForm
    template_name = 'core/resume_add.html'
    success_message = 'Вы успешно создали резюме'
    success_url = reverse_lazy('resume_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ResumeDetailView(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'core/resume_detail.html'
    context_object_name = 'resume'


class ResumeUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Resume
    form_class = ResumeAddForm
    template_name = 'core/resume_update.html'
    success_message = 'Вы успешно обновили резюме'
    success_url = reverse_lazy('resume_list')


class ResumeToArchive(View):
    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk)
        resume.status_resume = 'archive'
        resume.save()
        messages.success(request, 'Ваше резюме перенесено в архив')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ResumeToActive(View):
    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk)
        resume.status_resume = 'active'
        resume.save()
        messages.success(request, 'Ваше резюме перенесено из архива')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ResumeDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    # model = Resume
    # success_message = 'Вы успешно удалили резюме'
    # success_url = reverse_lazy('resume_list')
    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk)
        resume.delete()
        messages.success(request, 'Вы успешно удалили резюме')
        return redirect('resume_list')


################################################   Vacancy   ############################################################

class VacanciesView(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'core/vacancies.html'
    context_object_name = 'vacancies'


class VacancyListView(View):

    def get(self, request):
        all_vacancies = Vacancy.objects.filter(company=request.user)
        return render(request, 'core/vacancies_list.html', {'all_vacancies': all_vacancies})


class VacancyAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyAddForm
    template_name = 'core/vacancy_add.html'
    success_message = 'Вы успешно создали вакансию'
    success_url = reverse_lazy('vacancies_list')

    def form_valid(self, form):
        form.instance.company = self.request.user
        form.save()
        return super().form_valid(form)


class VacancyDetailView(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'core/vacancy_detail.html'
    context_object_name = 'vacancy'


class VacancyUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Vacancy
    form_class = VacancyAddForm
    template_name = 'core/vacansy_update.html'
    success_message = 'Вы успешно обновили вакансию'
    success_url = reverse_lazy('vacancies_list')


class VacancyToArchive(View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.get(pk=pk)
        vacancy.status_vacancy = 'archive'
        vacancy.save()
        messages.success(request, 'Ваша вакансия перенесена в архив')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class VacancyToActive(View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.get(pk=pk)
        vacancy.status_vacancy = 'active'
        vacancy.save()
        messages.success(request, 'Ваша вакансия перенесена из архива')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class VacancyDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, pk):
        vacancy = Vacancy.objects.get(pk=pk)
        vacancy.delete()
        messages.success(request, 'Вы успешно удалили вакансию')
        return redirect('vacancies_list')


############################################################################################################################

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        resume_id = request.POST.get('resume')
        resume = Resume.objects.get(pk=resume_id)
        vacancy = Vacancy.objects.get(pk=pk)
        # print(resume, vacancy)
        # print(type(resume))
        vacancy.followers.add(resume)
        messages.success(request, f'Отклик на вакансию успешно отправлен!')
        # notification = Notification.objects.create(notification_type=3, from_user=request.user,
        #                                            to_user=profile)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        # profile = Profile.objects.get(slug=slug)
        # profile.followers.remove(request.user)
        # messages.success(request, f'Вы успешно отписались от пользователя {profile.last_name} {profile.first_name}')
        # notification = Notification.objects.create(notification_type=4, from_user=request.user,
        #                                            to_user=profile.user)
        return redirect('profile', slug=profile.slug)


class ResponsesListView(TemplateView):
    template_name = 'core/responses.html'
