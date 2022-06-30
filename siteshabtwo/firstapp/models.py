from django.db import models
from django.contrib.auth.models import User


class ModelForWork(models.Model):
    title = models.CharField(max_length=70, verbose_name='Услуга')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    field_name = models.Field(help_text="Текст безвозмездной помощи", editable=True)
    email = models.EmailField(max_length=30, verbose_name='Почта')
    urlf = models.URLField(max_length=30, verbose_name='URL адрес')
    boolf = models.BooleanField(null=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['-title']
        unique_together = (
            ('title', 'content', 'published')
            ('title', 'price', 'email')
        )
        indexes = [
            models.Index(fields=['-published', 'title'],
                         name='%(app_label)s_%(class)_main'),
            models.Index(fields=['title', ' price', 'content']),
        ]



class TupleModel(models.Model):
    SORTS = (
        ('by', 'Покупаю'),
        ('se', 'Продаю'),
        ('tr', 'Обмениваю'),
    )
    sort = models.CharField(max_length=1, choices=SORTS, default='se')


class TupleModelFirst(models.Model):
    DESCRIPTION = (
        ('Покупка-продажа', (
            ('by', 'Покупаю'),
            ('se', 'Продаю'),
        )),
        ('Обмен', (
            ('tr', 'Обмениваю'),
        ))
    )
    desk = models.CharField(max_length=1, choices=DESCRIPTION, blank=True)


class ScrollStr(models.Model):
    class ScrollPagesStr(models.TextChoices):
        BUY = 'by', 'Куплю'
        SELL = 'se', 'Продам'
        EXCHANGE = 'ex', 'Обменяю'
        RENT = 're'
        __empty__ = 'Выберите тип публикуемого объявления'

    scrollvar = models.CharField(max_length=1, choices=ScrollPages.choices, default=ScrollPagesStr.__empty__)


class ScrollInt(models.Model):
    class ScrollPagesInt(models.IntegerChoices):
        BUY = 1, 'Куплю'
        SELL = 2, 'Продам'
        EXCHANGE = 3, 'Обменяю'
        RENT = 4
        __empty__ = 'Выберите тип публикуемого объявления'

    scrollvar = models.SmallIntegerField(max_length=1, choices=ScrollPages.choices, default=ScrollPagesInt.__empty__)


class ScrollVarious(models.Model):
    class ScrollPagesVar(float, models.Choices):
        METERS = 1.3332, 'Метры'
        FEET = 0.3232, 'Футы'
        YARDS = 3.22, 'Ярды'
        __empty__ = 'Выберите тип публикуемого объявления'

    scrollvar = models.FloatField(choices=ScrollPagesVar.choices)


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Machine(models.Model):
    name = models.CharField(max_length=30)


class SparePart(model.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(SparePart)

