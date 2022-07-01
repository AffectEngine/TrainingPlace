from django.db import models
from django.shortcuts import reverse


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


class Person(models.Model):
    choices = (
            ('M', 'Male'),
            ('F', 'Female')
        )
    name = models.CharField(max_length=10)
    sex = models.CharField(max_length=1, choices=choices)
    age = models.IntegerField()

    def get_absolute_url(self):
        return reverse('bboard:ppl', kwargs={'id': self.id, 'name': self.name})

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        ordering = ['name']

