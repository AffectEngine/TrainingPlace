from django.forms import ModelForm
from .models import FirstModel, Person
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
        fields = ('name', 'sex', 'age')