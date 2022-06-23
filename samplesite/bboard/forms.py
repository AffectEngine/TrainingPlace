from django.forms import ModelForm
from .models import FirstModel

class FirstModelForm(ModelForm):
    class Meta:
        model = FirstModel
        fields = ('title', 'content', ' price', 'rubric')
