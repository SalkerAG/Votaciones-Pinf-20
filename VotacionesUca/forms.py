#users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral,Opciones,Pregunta, Votacion, Eleccion
from django.contrib.admin.widgets import AdminDateWidget
  
c=[('0','Simple'),('1','Compleja')]
b=[('0','No'),('1','Sí')]

class ProcesoElectoralForm(forms.ModelForm):
    esConsulta=forms.ChoiceField(widget=forms.Select(), choices=b)
    fecha_inicio = forms.DateField(widget = forms.SelectDateWidget)
    fecha_fin = forms.DateField(widget = forms.SelectDateWidget)
    hora_inicio = forms.TimeField()
    hora_fin = forms.TimeField()
    nombreFicheroCenso=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Nombre del Censo'}),required=True)
    
    class Meta:
        model=ProcesoElectoral
        fields='__all__'

class PreguntaForm(forms.ModelForm):
    enunciado=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Pregunta para la votacion'}))

    class Meta:
        model=Pregunta
        fields='__all__'

class VotacioneForm(ProcesoElectoralForm):
    nombreVotacion=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Título de la votación'}))
    esPresencial=forms.ChoiceField(widget=forms.Select(), choices=b)
    votoRectificable=forms.ChoiceField(widget=forms.Select(), choices=b)
    tipoVotacion=forms.ChoiceField(label='Tipo de votacion',choices=c)
    maxElector=forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escribe el número máximo de respuestas'}),min_value=0)

    class Meta:
        model=Votacion
        fields= '__all__'


