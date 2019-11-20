# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import UsuarioUca
from django.core.validators import RegexValidator
from django.core.validators import validate_slug, validate_email


class CustomUserCreationForm(UserCreationForm):
    # isnumericvalidator = RegexValidator(r"[1-9][0-9]*|0",
    #                                     message='El NIF debe ser numérico',
    #                                     code='NIF invalido')
    nif = forms.CharField(label='NIF', max_length=9, widget=forms.TextInput(attrs={"placeholder": "Ej:32085090"}))
                          # validators=[isnumericvalidator])
    email = forms.EmailField(label='Email', max_length=64, help_text="El correo debe pertener al dominio de la UCA",
                             required=True)
    first_name = forms.CharField(label="Nombre", max_length=20, required=True)
    last_name = forms.CharField(label="Apellidos", max_length=64, required=True)

    class Meta:
        model = UsuarioUca
        fields = '__all__'

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.nif = "u" + user.nif
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UsuarioUca
        fields = '__all__'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'password',
        }
    ))
