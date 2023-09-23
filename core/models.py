from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

from users.models import User

STATUS = [
    ('active', 'Активный'),
    ('archive', 'Архив'),
]


class Vacancy(models.Model):
    '''Вакансия'''

    company = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='компания', related_name='all_vakancies')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='vacansies', verbose_name='Категория')
    job_title = models.CharField('должность', max_length=300)
    description = CKEditor5Field('описание', max_length=1000, blank=True, null=True, config_name='extends')
    charge = CKEditor5Field('обязанности', max_length=2500, blank=True, null=True, config_name='extends')
    conditions = CKEditor5Field('условия', blank=True, null=True, config_name='extends')
    min_price = models.SmallIntegerField('мин зарплата')
    max_price = models.SmallIntegerField('макс зарплата')
    stack = TaggableManager('стек технологий', blank=True)
    date = models.DateTimeField('время публикации', default=timezone.now)
    status_vacancy = models.CharField('статус вакансии', choices=STATUS, max_length=300)
    followers = models.ManyToManyField('Resume', verbose_name='отклики', blank=True, related_name='followers')
    required_experience = models.CharField('требуемый опыт', max_length=1000, blank=True, null=True)
    slug = models.SlugField('слаг', unique=True, blank=True, null=True)

    related_name = 'followers'

    def __str__(self):
        return f'Вакансия {self.job_title} от {self.company.account.fullname}'

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def clean(self):
        if self.min_price > self.max_price:
            raise ValidationError("Минимальная зарплата не может быть больше максимальной")


class Category(MPTTModel):
    '''Категория'''
    title = models.CharField(max_length=1000, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    #
    # def get_absolute_url(self):
    #     return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return f'{self.title}'


class Experience(models.Model):
    '''Опыт работы'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='experiences')
    job_title = models.CharField('должность', max_length=300)
    name_company = models.CharField('компания', max_length=300)
    charge = models.CharField('обязанности', max_length=300)
    start_work = models.DateField('начало работы')
    end_work = models.DateField('конец работы')
    stack = TaggableManager('стек технологий', blank=True)

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = "Опыт работы"

    # def __str__(self):
    #     return self.user.username


class Resume(models.Model):
    '''Резюме'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='all_resume')
    image = models.ImageField(upload_to='users/resume', null=True, blank=True, default='default/default.jpg')
    job_title = models.CharField('должность', max_length=300)
    description = CKEditor5Field('о себе', max_length=1000, blank=True, config_name='extends')
    skills = CKEditor5Field('навыки', max_length=300, blank=True, null=True, config_name='extends')
    experience = models.ManyToManyField(Experience, blank=True, verbose_name='опыт работы')
    min_price = models.SmallIntegerField('мин зарплата')
    max_price = models.SmallIntegerField('макс зарплата')
    stack = TaggableManager('стек технологий', blank=True)
    date = models.DateTimeField('дата публикации', default=timezone.now)
    responses = models.ManyToManyField(Vacancy, verbose_name='отклики', blank=True)
    status_resume = models.CharField('статус вакансии', choices=STATUS, max_length=300, default='active')

    def clean(self):
        if self.min_price > self.max_price:
            raise ValidationError("Минимальная зарплата не может быть больше максимальной")

    # def __str__(self):
    #     return f'Резюме {self.job_title} от {self.user.account.fullname}'

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Все резюме'


class FeedBack(models.Model):
    email = models.EmailField('почта')
    name = models.CharField('имя', max_length=150)
    theme = models.CharField('тема', max_length=500)
    text = models.TextField('тест обращения')
    image = models.ImageField('скриншот', upload_to='feedback/screen', blank=True)

    def __str__(self):
        return f'Обратная связь от {self.name} | {self.email}'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class PersonFavorites(models.Model):
    '''Избранное пользователя'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь',
                                related_name='person_favorites')
    vacancy = models.ForeignKey(Vacancy, verbose_name='вакансия', on_delete=models.CASCADE, )


class CompanyFavorites(models.Model):
    '''Избранное компании'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь',
                                related_name='company_favorites')
    resume = models.ManyToManyField(Resume, verbose_name='резюме', blank=True, related_name='resume')
