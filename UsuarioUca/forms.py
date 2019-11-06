# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioUca


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioUca
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UsuarioUca
        fields = '__all__'
