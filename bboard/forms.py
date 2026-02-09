from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelform_factory, DecimalField, modelformset_factory
from django.forms.widgets import Select
from bboard.models import Bb, Rubric


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


# BbForm = modelform_factory(
#     Bb,
#     fields=('title', 'content', 'price', 'rubric'),
#     labels={'title': 'Название товара'},
#     help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
#     field_classes={'price': DecimalField},
#     widgets={'rubric': Select(attrs={'size': 8})}
# )


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'}
#         help_texts = {'rubric': 'Не забудьте выбрать рубрику!'}
#         field_classes = {'price': DecimalField}
#         widgets = {'rubric': Select(attrs={'size': 8})}


# class BbForm(ModelForm):
#     title = forms.CharField(label='Название товара')
#
#     content = forms.CharField(
#         label='Описание',
#         widget=forms.widgets.Textarea()
#     )
#
#     price = forms.DecimalField(
#         label='Цена',
#         decimal_places=2
#     )
#
#     rubric = forms.ModelChoiceField(
#         queryset=Rubric.objects.all(),
#         label='Рубрика',
#         help_text='Не забудьте выбрать рубрику!',
#         widget=forms.widgets.Select(attrs={'size': 8})
#     )
#
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


class BbForm(ModelForm):
    title = forms.CharField(
        label='Название товара',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Слишком короткое название товара'}
    )

    price = forms.DecimalField(
        label='Цена',
        decimal_places=2
    )
    rubric = forms.ModelChoiceField(
        queryset=Rubric.objects.all(),
        label='Рубрика',
        help_text='Не забудьте выбрать рубрику!',
        widget=forms.widgets.Select(attrs={'size': 8})
    )
    # captcha = CaptchaField(
    #     # generator='captcha.helpers.math_challenge',
    #     label='Введите текст с картинки',
    #     error_messages={'invalid': 'Неправильный текст'}
    # )

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Прошлогодний снег':
            raise ValidationError('К продаже не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}

        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')

        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')

        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        labels = {'title': 'Название товара'}


RubricFormSet = modelformset_factory(
    Rubric,
    fields=('name',),
    can_order=True,
    can_delete=True,
)


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')
