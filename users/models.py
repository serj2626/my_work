from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField

TYPE_USER = [
    ('person', 'Частное лицо'),
    ('company', 'Компания')
]


class User(AbstractUser):
    email = models.EmailField('почта', unique=True)
    type = models.CharField('тип пользователя', max_length=15, choices=TYPE_USER)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'Пользователь {self.email} {self.username}'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь',
                                related_name='account')
    fullname = models.CharField('Имя пользователя', max_length=1000, blank=True, null=True)
    data_client = models.IntegerField('данные клиента', blank=True, null=True)
    country = CountryField('страна', null=True, blank=True)
    image = models.ImageField(upload_to='users/accounts', null=True, blank=True, default='default/default.jpg')
    slug = models.SlugField('слаг', blank=True)

    class Meta:
        verbose_name = 'Аккаунт пользователя'
        verbose_name_plural = "Аккаунты пользователей"

    def __str__(self):
        return f'Аккаунт пользователя {self.fullname}'

    def save(self, *args, **kwargs):
        email = self.user.email.lower()
        ind = email.index('@')
        self.slug = email[:ind]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:account', kwargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()

# class Notification(models.Model):
#     '''Уведомления'''
#
#     # 1 = Вам отказали, 2 = Вас пригласили, 3 = Вакансия перенесена в архив 4 = Вам оставили сообщение
#     # notification_type = models.IntegerField(verbose_name='тип', validators=[MinValueValidator(1), MaxValueValidator(3)])
#
#     NOTIFICATION_TYPE = [
#         (1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Unsubscribe')
#     ]
#
#     notification_type = models.IntegerField(verbose_name='тип', choices=NOTIFICATION_TYPE, default=1)
#     to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True,
#                                 verbose_name='уведомление_кому')
#     from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True,
#                                   verbose_name='уведомление_от')
#     image = models.ForeignKey('ProfileImage', on_delete=models.CASCADE, related_name='+', blank=True, null=True,
#                               verbose_name='фото')
#
#     date = models.DateTimeField(default=timezone.now, verbose_name='дата')
#     user_has_seen = models.BooleanField(default=False, verbose_name='прочитано?')
#
#     class Meta:
#         verbose_name = 'Уведомление'
#         verbose_name_plural = 'Уведомления'
#
#     def __str__(self):
#         return f'Уведомление от {self.from_user} кому {self.to_user} от {self.date}'


# class PersonFavorites(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь',
#                                 related_name='person_favorites')
#     vacancies = models.ManyToManyField(Vacancy, verbose_name='вакансии', blank=True, related_name='vacancies')
#
#
# class CompanyFavorites(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь',
#                                 related_name='company_favorites')
#     resume = models.ManyToManyField(Resume, verbose_name='резюме', blank=True, related_name='resume')
