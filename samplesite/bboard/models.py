from django.db import models
from django.shortcuts import reverse
from django.core import validators
from django.core.exceptions import ValidationError
# from datetime import date


class FirstModel(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']

    def title_and_price(self):
        if self.price:
            return f"{self.title} {self.price}"
        else:
            return self.title

    title_and_price.short_description = 'Название и цена'


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


def get_min_length():
    min_length = 1
    return min_length


def get_min_age():
    min_age = 18
    return min_age


class Person(models.Model):
    choices = (
            ('M', 'Male'),
            ('F', 'Female')
        )
    name = models.CharField(max_length=10, verbose_name='Имя', validators=[validators.MinLengthValidator(get_min_length)])
    sex = models.CharField(max_length=1, verbose_name='Пол', choices=choices)
    birth_date = models.DateField(verbose_name='Дата рождения', default='2022-07-02')
    age = models.IntegerField(verbose_name='Возраст', validators=[validators.MinValueValidator(get_min_age, message='Регистрация доступна пользователям с 18 лет')])
    mail = models.EmailField(max_length=30, verbose_name='Почта', default=' ', validators=[validators.EmailValidator(message='Некорректный ввод')])
    git = models.URLField(max_length=90, verbose_name='Ссылка на Git', default=' ', validators=[validators.URLValidator(schemes=None, regex='github.com', message='Введите корректный Git адрес', code='invalid')])

    def get_absolute_url(self):
        return reverse('bboard:ppl', kwargs={'id': self.id, 'name': self.name})

    def clean(self):
        errors = {}
        try:
            if self.age < 0:
                errors['age'] = ValidationError('Возраст не может быть отрицательным')
        except TypeError:
            print('Пустая строка ввода возраста')

        if not self.name:
            errors['name'] = ValidationError('Укажите ваше имя')

        if errors:
            raise ValidationError(errors)

    # def calculate_age(born):
    #     today = date.today()
    #     return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        ordering = ['name']

    # def clean(self):
    #     errors = {}
    #     try:
    #         if self.age < 0:
    #             errors['age'] = ValidationError('Возраст не может быть отрицательным')
    #     except TypeError:
    #         print('Пустая строка ввода возраста')