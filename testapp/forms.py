from django import forms
from django.contrib.auth.models import User
from django.core import validators

from testapp.models import Img


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email',
                  'password1', 'password2',
                  'first_name', 'last_name')


class ImgForm(forms.ModelForm):
    img = forms.ImageField(
        label='Изображение',
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('gif', 'jpg', 'png'))],
        error_messages={
            'invalid_extension': 'Этот формат не поддерживается'}
    )

    desc = forms.CharField(
        label='Описание',
        widget=forms.widgets.Textarea()
    )

    class Meta:
        model = Img
        fields = '__all__'
