#users/forms.py
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django import forms
from .views import CrearVotacionView
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones

def positivo(value):
   if value<=0:
      raise ValidationError('El número debe ser mayor que 0.')

c=[('0','Simple'),('1','Compleja')]

class FormProcesoElectoral(forms.ModelForm):
    create_at=forms.DateTimeField()
    update_at=forms.DateField()
    esConsulta=forms.BooleanField(label='Consulta',initial=False)
    fechaInicio=forms.DateTimeField(label='Fecha Inicio del proceso electoral',required=True)
    fechaFin=forms.DateTimeField(label='Fecha Fin del proceso electoral',required=True)
    nombreFicheroCenso=forms.CharField(required=True)

    class Meta:
        model=ProcesoElectoral
        fields='__all__'


class PreguntaForm(forms.ModelForm):
    enunciado=forms.CharField(max_length=50,required=True)
    opciones=forms.ManyToManyField(Opciones())

    class Meta:
        model=Pregunta
        fields='__all__'

class VotacioneForm(forms.ModelForm):
    proceso=FormProcesoElectoral()
    pregunta=PreguntaForm()
    esPresencial=forms.BooleanField(label='Proceso Electoral presencial',initial=False)
    votoRectificable=forms.BooleanField(label='Voto rectificable',initial=False)
    tipoVotacion=forms.ChoiceField(label='Tipo de votacion',choices=c)
    maxElector=forms.IntegerField(label='Numero maximo de electores',validators=[positivo],min_value=0)

    class Meta:
        model=Votacione
        fields='__all__'