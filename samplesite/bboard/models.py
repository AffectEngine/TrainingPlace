from django.db import models
from django.shortcuts import reverse
from django.core import validators
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class FirstModel(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика',
                               related_query_name='FMfilter')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-rubric']
        get_latest_by = 'published'


# Плохая практика комментария блока кода. метод можно использовать для отображения названия-цены одновременно

# def title_and_price(self):
#     if self.price:
#         return f"{self.title} {self.price}"
#     else:
#         return self.title
#
# title_and_price.short_description = 'Название и цена'


class Rubric(models.Model):
    name = models.CharField(
        max_length=30, db_index=True, verbose_name='Название',
        validators=[validators.MinLengthValidator(2, message='Название слишком короткое!')]
    )
    owner = models.ForeignKey('Person', null=True, on_delete=models.PROTECT, verbose_name='Собственник',
                              related_query_name='Pfilter')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


def get_min_length():
    min_length = 1
    return min_length


class Person(models.Model):
    choices = (
        ('M', 'Женщина'),
        ('F', 'Мужчина'),
        ('N', 'Неопределенный')
    )
    name = models.CharField(max_length=15, verbose_name='Имя',
                            validators=[validators.MinLengthValidator(get_min_length)])
    second_name = models.CharField(max_length=15, verbose_name='Второе имя', default='',
                                   validators=[validators.MinLengthValidator(get_min_length)])
    skin_color = models.CharField(max_length=15, verbose_name='Цвет кожи', default='',
                                  validators=[validators.MinLengthValidator(get_min_length)], blank=True, null=True)
    sex = models.CharField(max_length=1, verbose_name='Пол', choices=choices)
    age = models.IntegerField(verbose_name='Возраст')
    mail = models.EmailField(max_length=30, verbose_name='Почта', default=' ',
                             validators=[validators.EmailValidator(message='Некорректный ввод')])
    git = models.URLField(max_length=90, verbose_name='Ссылка на Git', default=' ', validators=[
        validators.URLValidator(schemes=None, regex='github.com', message='Введите корректный Git адрес',
                                code='invalid')], blank=True, null=True)

    def __str__(self):
        return self.name

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

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        ordering = ['name']


class Spare(models.Model):
    name = models.CharField(max_length=30)
    notes = GenericRelation('Note')

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit')
    notes = GenericRelation('Note')

    def __str__(self):
        return self.name


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')


# ПРЯМОЕ ( МНОГОТАБЛИЧНОЕ ) НАСЛЕДОВАНИЕ
class Message(models.Model):
    content = models.TextField()


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, parent_link=True)


# АБСТРАКТНОЕ НАСЛЕДОВАНИЕ
class Specification(models.Model):
    title = models.TextField(max_length=40)
    pages = models.PositiveIntegerField()
    author = models.TextField(max_length=40)

    class Meta:
        abstract = True
        ordering = ['title']


class VIPSpecification(Specification):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=40)
    pages = None

    class Meta(Specification.Meta):
        pass

