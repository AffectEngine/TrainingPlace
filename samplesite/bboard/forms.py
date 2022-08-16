from django.forms import ModelForm, modelform_factory, DecimalField, modelformset_factory
from django.forms.widgets import Select
from django.forms import modelformset_factory
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from .models import FirstModel, Person, Rubric

BIRTH_YEARS_FOR_CHOICE = ['1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960',
                          '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971',
                          '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982',
                          '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993',
                          '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
                          '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',
                          '2016', '2017', '2018', '2019', '2020', '2021']

RARITY = [
    ('a', 'Обычное'),
    ('b', 'Необычное'),
    ('c', 'Редкое'),
]


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'second_name', 'skin_color', 'sex', 'age', 'mail', 'git')


class FirstModelFullForm(forms.ModelForm):
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика',
                                    help_text='Не забудьте задать рубрику!',
                                    widget=forms.widgets.RadioSelect())
    item_rarity = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=RARITY,
    )

    class Meta:
        model = FirstModel
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}


    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if self.cleaned_data['title'] == 'Снег':
            errors['title'] = ValidationError('Не допускается к продаже')
        if errors:
            raise ValidationError(errors)




class RegisterPersonForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', min_length=8, max_length=20)
    password2 = forms.CharField(label='Повторите пароль', min_length=8, max_length=20)
    date_birth = forms.DateField(label='Дата рождения',
                                 widget=forms.widgets.SelectDateWidget(empty_label=('Год', 'Месяц', 'Число'),
                                                                       years=(BIRTH_YEARS_FOR_CHOICE)))
    age = forms.IntegerField(label='Возраст', validators=[
        validators.MinValueValidator(18)], error_messages={'invalid': 'Регистрация доступна пользователям с 18 лет'})

    class Meta:
        model = Person
        fields = (
            'name', 'second_name', 'date_birth', 'age', 'password1', 'password2', 'mail', 'skin_color', 'sex', 'git')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("Повторите пароль")
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
