from django.forms import ModelForm, modelform_factory, DecimalField
from django.forms.widgets import Select
from django import forms

from .models import FirstModel, Person, Rubric


# from urllib import request
# from django.core.files.base import ContentFile
# from django.utils.text import slugify


class FirstModelForm(ModelForm):
    class Meta:
        model = FirstModel
        fields = ('title', 'content', 'price', 'rubric')


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'second_name', 'skin_color', 'sex', 'age', 'mail', 'git')


class FirstModelFullForm(forms.ModelForm):
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика',
                                    help_text='Не забудьте задать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = FirstModel
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}


class RegisterPersonForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повторите пароль')

    class Meta:
        model = Person
        fields = ('name', 'second_name', 'skin_color', 'sex', 'age', 'password1', 'password2', 'mail', 'git')
