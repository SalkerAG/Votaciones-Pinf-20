# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioUca




class CustomUserCreationForm(UserCreationForm):
    dni = forms.CharField(label='Dni', max_length=9, widget=forms.TextInput(attrs={"placeholder": "Ej:32085090K"}))
    class Meta:
        model = UsuarioUca
        fields = '__all__'




class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UsuarioUca
        fields = '__all__'


