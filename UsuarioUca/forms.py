
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelForm


from .models import UsuarioUca, uvalidonifworld, uvalidonifspain, validonifspain, validonifworld, Estudiante, PASS, \
    Profesor
from django.core.validators import RegexValidator


istextvalidator = RegexValidator("^(?=.{3,15}$)[A-ZÁÉÍÓÚ][a-zñáéíóú]+(?: [A-ZÁÉÍÓÚ][a-zñáéíóú]+)?$",
                                 message='El Nombre no debe contener números',
                                 code='Nombre/Apellidos incorrectos')
isemailvalidator = RegexValidator("^\w+([\.-]?\w+)*@alum.uca.es",
                                  message='El email debe pertenecer al dominio de la UCA',
                                  code='Email invalido')





class CustomUserCreationForm(UserCreationForm):
    nif = forms.CharField(label='NIF', max_length=9, widget=forms.TextInput(attrs={"placeholder": "Ej:32085090"}))

    email = forms.EmailField(label='Email', max_length=64, help_text="El correo debe pertener al dominio de la UCA",
                             required=True, validators=[isemailvalidator])
    first_name = forms.CharField(label="Nombre", max_length=20, min_length=2, required=True,
                                 validators=[istextvalidator])
    last_name = forms.CharField(label="Apellidos", max_length=64, min_length=2, required=True,
                                validators=[istextvalidator])

    class Meta:
        model = UsuarioUca
        fields = '__all__'



    def clean_nif(self):
        nif = self.cleaned_data['nif']
        nif = "u" + nif
        if UsuarioUca.objects.filter(nif=nif).exists():
            raise forms.ValidationError("Ya existe un usuario con este NIF")
        return nif


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(label='Email', max_length=64,
                             required=True)
    nif = forms.CharField(label="Nif", required=True, max_length=10)
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

class createUserForm(ModelForm):
    class Meta:
        model = UsuarioUca
        fields = ['nif', 'first_name', 'last_name', 'email', 'password', 'rol']
        labels = {'first_name': ('Nombre'), 'last_name': ('Apellidos'), 'nif': ('NIF'),
                  'email': ('Correo electrónico'), 'password': ('Contraseña'), 'rol': ('Rol'), }
        help_texts = {'first_name': ('Introduce un nombre valido.'), 'last_name': ('Introduce los apellidos válidos.'),
                      'nif': ('Introduce un nif válido'),
                      'email': ('Introduce un correo válido y del dominio de la UCA'),
                      'groups': ('Grupo al que pertenece el usuario'), }

        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'nif': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control'}), }



    def clean_nif(self):
        nif = self.cleaned_data['nif']
        nif = "u" + nif
        if UsuarioUca.objects.filter(nif=nif).exists():
            raise forms.ValidationError("Ya existe un usuario con este NIF")
        return nif

    def save(self, commit=True):
        user = super(createUserForm, self).save()

        user.set_password(user.password)


        user.save()

        return user


class editUserForm(ModelForm):
    class Meta:
        model = UsuarioUca
        fields = ['nif', 'first_name', 'last_name', 'email',

                  ]
        labels = {'first_name': ('Nombre'), 'last_name': ('Apellido'), 'nif': ('NIF'),
                  'email': ('Correo electrónico'),

                  }


        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'nif': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),

                   }


