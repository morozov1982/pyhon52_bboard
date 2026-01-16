from django import forms
from django.contrib.auth.models import User


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email',
                  'password1', 'password2',
                  'first_name', 'last_name')
