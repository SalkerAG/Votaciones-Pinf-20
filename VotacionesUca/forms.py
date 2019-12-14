#users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion

def positivo(value):
   if value<=0:
      raise ValidationError('El número debe ser mayor que 0.')

c=[('0','Simple'),('1','Compleja')]

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    attrs={}

class ProcesoElectoralForm(forms.ModelForm):
    create_at=forms.DateTimeField() 
    update_at=forms.DateTimeField()
    esConsulta=forms.BooleanField()
    fechaInicio=forms.DateTimeField(required=True, widget=DateTimeInput)
    fechaFin=forms.DateTimeField(required=True, widget=DateTimeInput)
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
    proceso=ProcesoElectoralForm()
    pregunta=PreguntaForm()
    nombreVotacion=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Título de la votación'}))
    esPresencial=forms.BooleanField()
    votoRectificable=forms.BooleanField()
    tipoVotacion=forms.ChoiceField(label='Tipo de votacion',choices=c)
    maxElector=forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escribe el número máximo de respuestas'}), validators=[positivo],min_value=0)

    class Meta:
        model=Votacione
        fields='__all__'