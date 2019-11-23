# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import UsuarioUca, uvalidonifworld, uvalidonifspain
from django.core.validators import RegexValidator
from django.core.validators import validate_slug, validate_email

istextvalidator = RegexValidator("^[a-zA-Z0]*$",
                                 message='El Nombre no debe contener números',
                                 code='Nombre invalido')

# isnumericvalidator = RegexValidator(r"[1-9][0-9]*|0",
#                                     message='El NIF debe ser numérico',
#                                     code='NIF invalido')


class CustomUserCreationForm(UserCreationForm):


    nif = forms.CharField(label='NIF', max_length=10, widget=forms.TextInput(attrs={"placeholder": "Ej:32085090"}))
    # validators=[isnumericvalidator])
    email = forms.EmailField(label='Email', max_length=64, help_text="El correo debe pertener al dominio de la UCA",
                             required=True)
    first_name = forms.CharField(label="Nombre", max_length=20, required=True, validators=[istextvalidator])
    last_name = forms.CharField(label="Apellidos", max_length=64, required=True, validators=[istextvalidator])

    class Meta:
        model = UsuarioUca
        fields = '__all__'

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        # user.nif = "u" + user.nif
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    first_name = forms.CharField(label="Nombre", max_length=20, required=True, validators=[istextvalidator])
    last_name = forms.CharField(label="Apellidos", max_length=64, required=True, validators=[istextvalidator])
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
