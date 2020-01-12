
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral, Pregunta, Votacion, Eleccion, Censo, UsuarioVotacion, OpcionesCompleja, \
    UsuarioEleccion, Personas
from bootstrap_modal_forms.forms import BSModalForm





class ProcesoElectoralForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control inputstl', 'placeholder': 'Select Date'}))
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control inputstl', 'placeholder': 'Select Date'}))

    es_consulta = forms.BooleanField(required=False)
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control inputstl'}))
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control inputstl'}))

    class Meta:
        model = ProcesoElectoral
        fields = ('__all__')


class OpcionesSimpleForm(forms.ModelForm):
    pass


class OpcionesComplejaForm(forms.ModelForm):
    class Meta:
        model = OpcionesCompleja
        fields = ('respuesta', )
        labels = {'respuesta': ('Respuesta')}
        help_texts = {'respuesta': (
            'Añada las respuestas que perteneceran a las opciones disponibles de la votación'),
        }
        widgets = {'respuesta': forms.TextInput(attrs={'class': 'form-control'}),
                   }



class VotacionForm(ProcesoElectoralForm):
    voto_restringido = forms.BooleanField(required=False)
    nombre_votacion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la votacion'}), required=True)
    es_presencial = forms.BooleanField(required=False)
    voto_rectificable = forms.BooleanField(required=False)

    class Meta:
        model = Votacion
        fields = ('__all__')




class createCensoForm(ModelForm):
    class Meta:
        model = Censo
        fields = ('__all__')
        labels = {'usuario': ('Usuarios pertenecientes al censo'), 'pregunta': ('Pregunta'), }
        help_texts = {'usuario': (
            'Elige los usuarios que pertenecen al censo. Recuerda que serán los usuarios que tendrán acceso a la votación'),
            'pregunta': ('Elige la pregunta a la que hace referencia el censo'),
        }

        widgets = {'usuario': forms.SelectMultiple(attrs={'class': 'form-control'}),
                   'pregunta': forms.Select(attrs={'class': 'form-control'}),
                   }


class realizarVotacionForm(ModelForm):
    # usuario = models.ForeignKey("auth.User", blank=True)
    CHOICES = (('Si', 'Si'), ('No', 'No'), ('Abstención', 'Abstención'))
    seleccion = forms.ChoiceField(choices=CHOICES)
    #seleccion = forms.ChoiceField(label='', choices=CHOICES, widget=forms.Select(attrs={'class':'regDropDown'}))

    class Meta:
        model = UsuarioVotacion
        fields = 'user', 'Votacion', 'Pregunta', 'seleccion'
        labels = {'user': (''), 'Votacion': (''), 'Pregunta': (''), 'seleccion': ('Respuesta'), }
        widgets = {'user': forms.Select(
            attrs={'disabled': 'disabled', 'class': 'bootstrap-select', 'hidden': 'hidden', }),
            'Votacion': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'Pregunta': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'seleccion': forms.Select(attrs={'class': 'form-control'}),
        }



class realizarVotacionComplejaForm(ModelForm):

    qs = OpcionesCompleja.objects.all().values_list('respuesta', flat=True)

    opcionesCompleja = forms.ModelChoiceField(qs, label='Respuesta:')

    class Meta:
        model = OpcionesCompleja
        fields = ('Pregunta', )
        labels = {'respuestasComplejas': ('Respuesta') }
        widgets = {'Votacion': forms.Select(
            attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'Pregunta': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'seleccion': forms.Select(attrs={'class': 'form-control'}),

        }



class PreguntaForm(BSModalForm):
    class Meta:
        model = Votacion
        fields = ('__all__')



class PreguntaFormVotacion(ModelForm):
    class Meta:
        model = Pregunta
        fields = 'Votacion', 'tipo_votacion', 'enunciado',
        labels = {'Votacion': (''), 'enunciado': ('Enunciado'), }
        widgets = {'Votacion': forms.Select(
            attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'Votacion': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'Pregunta': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'seleccion': forms.Select(attrs={'class': 'form-control'}),
        }

class EleccionForm(ProcesoElectoralForm):
    nombre= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la elección'}))
    max_vacantes= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rellenar con un valor 0 a 1, válido solo para Grupos. Ej: 0.7'}))

    class Meta:
        model = Eleccion
        fields = '__all__'




class realizarEleccionForm(ModelForm):
    qs = Personas.objects.all().values_list('nombre', flat=True)
    seleccion = forms.ModelChoiceField(qs, label='Seleccion:')

    class Meta:
        model = UsuarioEleccion
        fields = 'seleccion',

        labels = {'user': (''), 'Eleccion': (''), }
        widgets = {'Votacion': forms.Select(
            attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'Votacion': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'Pregunta': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control', 'hidden': 'hidden', }),
            'seleccion': forms.Select(attrs={'class': 'form-control'}),

        }


class PersonaForm(ModelForm):

    class Meta:
        model = Personas
        fields = ('nombre',)
        labels = {'nombre': ('Nombre del candidato')}
        help_texts = {'nombre': ('Añada uno por uno el nombre de los candidatos a la elección que se muestra en la parte superior')}
        widgets = {'nombre': forms.TextInput(
            attrs={'class': 'form-control', }),
        }


class ListaVotacionForm(ModelForm):
    class Meta:
        model = Votacion
        fields = ('__all__')

class ListaEleccionForm(ModelForm):
    class Meta:
        model = Eleccion
        fields = ('__all__')

class ListaCensoForm(ModelForm):
    class Meta:
        model = Censo
        fields = ('__all__')
