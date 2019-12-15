#users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion
from datetime import datetime
from .myfields import EuDateFormField
from datetime import datetime

fech='null'

def positivo(value):
   if value<=0:
      raise ValidationError('El número debe ser mayor que 0.')

def fech1(value):
    fech=value.strftime('%Y-%m-%d %H:%M:%S')
    if value.strftime('%Y-%m-%d %H:%M:%S')<=datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
        raise ValidationError('La fecha ser mayor que la actual.')

def fech2(value):
    if fech>=value.strftime('%Y-%m-%d %H:%M:%S'):
        raise ValidationError('La fecha de Fin debe ser mayor a la de Inicio.')    

c=[('0','Simple'),('1','Compleja')]

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    attrs={}

class ProcesoElectoralForm(forms.ModelForm):
    esConsulta=forms.BooleanField()
    fechaInicio=EuDateFormField(required=True,validators=[fech1])
    fechaFin=EuDateFormField(required=True,validators=[fech1,fech2])
    nombreFicheroCenso=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Nombre del Censo'}),required=True)


    class Meta:
        model=ProcesoElectoral
        fields='__all__'

class PreguntaForm(forms.ModelForm):
    enunciado=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Pregunta para la votacion'}))
    opciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Opciones a responder'}))

    class Meta:
        model=Pregunta
        fields='__all__'

class VotacioneForm(ProcesoElectoralForm, PreguntaForm):
    nombreVotacion=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Título de la votación'}))
    esPresencial=forms.BooleanField()
    votoRectificable=forms.BooleanField()
    tipoVotacion=forms.ChoiceField(label='Tipo de votacion',choices=c)
    maxElector=forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escribe el número máximo de respuestas'}), validators=[positivo],min_value=0)

    class Meta:
        model=Votacione
        fields='__all__'
        