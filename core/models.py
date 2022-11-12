from django.db import models
from django.contrib import admin
from django.db import models
from django.urls import reverse


class Person(models.Model):

    GENDER_CHOICES = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )

    surname = models.CharField('Фамилия', max_length=255)
    name = models.CharField('Имя', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255)
    date = models.DateField('Дата рождения', null=True)
    phone = models.PositiveSmallIntegerField('Номер телефона', blank=True, null=True)  # не CharField ???
    health = models.CharField('Состояние здоровья', blank=True,
                              default='Практически здоров', max_length=255,
                              help_text='аллергоанамнез, хронические заболевания и т.п.')
    gender = models.CharField('Ваш пол', max_length=1, choices=GENDER_CHOICES, default='M')
    image = models.ImageField('Ваша фотография', blank=True, upload_to='project/media') #

    class Meta:
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'
        ordering = ('surname', 'name', 'patronymic')

    def __str__(self):
        return f'{self.surname}-{self.name}-{self.patronymic}-{self.date}-{self.health}'

    def get_absolute_url(self):
        return reverse("core:base")


class EmergencyService(models.Model):
    name = models.CharField('Название', max_length=100)
    code = models.IntegerField('Код', help_text='01-Пожарная служба, 02-Полиция, 03-Скорая помощь', null=True)
    phone = models.CharField('Номер телефона', max_length=11)
    appeal = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='emergencyservices', null=True)  # Должно ли быть отношение ???

    class Meta:
        verbose_name = 'Экстренная служба'
        verbose_name_plural = 'Экстренные службы'
        ordering = ('code',)

    def __str__(self):
        return f'{self.name}-{self.code}-{self.phone}-{self.appeal}'

    def get_absolute_url(self):
        return reverse("core:base")


class Incident(models.Model):
    STATUS_CHOICE_IN_WORK = 'in_work'
    STATUS_CHOICE_COMPLETED = 'completed'
    STATUS_CHOICES = (
        (STATUS_CHOICE_IN_WORK, 'В работе'),
        (STATUS_CHOICE_COMPLETED, 'Завершено'),
    )

    date = models.DateTimeField('Дата обращения', auto_now_add=True)
    number = models.IntegerField('Номер обращения', blank=True, unique=True,
                                 db_index=True, editable=False, null=True)
    service = models.ManyToManyField(EmergencyService, null=True, related_name='incidents')
    victims = models.PositiveSmallIntegerField('Количество пострадавших', blank=True)
    call = models.BooleanField('Звонок', default=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CHOICE_IN_WORK)
    applicant = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='incidents', null=True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ('date', 'number')

    def __str__(self):
        return f'{self.date}-{self.number}-{self.service}-{self.applicant}'

    def get_absolute_url(self):
        return reverse('core:base')
