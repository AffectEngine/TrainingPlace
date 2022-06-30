from django.forms import ModelForm
from .models import FirstModel, Person

class FirstModelForm(ModelForm):
    class Meta:
        model = FirstModel
        fields = ('title', 'content', 'price', 'rubric')


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'sex', 'age')