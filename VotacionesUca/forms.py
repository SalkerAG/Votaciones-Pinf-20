#users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral,Opciones,Pregunta, Votacione, Eleccion
from datetime import datetime
from .myfields import EuDateFormField
from datetime import datetime
  
c=[('0','Simple'),('1','Compleja')]

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ProcesoElectoralForm(forms.ModelForm):
    esConsulta=forms.BooleanField()
    fechaInicio=forms.DateTimeField(required=True))
    fechaFin=EuDateFormField(required=True)
    nombreFicheroCenso=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Nombre del Censo'}),required=True)
    
    class Meta:
        model=ProcesoElectoral
        fields='__all__'

class OpcionesForm(forms.ModelForm):
    opciones = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Opciones a responder'}))

    class Meta:
        model=Opciones
        fields='__all__'

class PreguntaForm(forms.ModelForm):
    enunciado=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Pregunta para la votacion'}))

    class Meta:
        model=Pregunta
        fields='__all__'

class VotacioneForm(ProcesoElectoralForm, PreguntaForm):
    nombreVotacion=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Título de la votación'}))
    esPresencial=forms.BooleanField()
    votoRectificable=forms.BooleanField()
    tipoVotacion=forms.ChoiceField(label='Tipo de votacion',choices=c)
    maxElector=forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escribe el número máximo de respuestas'}),min_value=0)

    class Meta:
        model=Votacione
        fields=['esConsulta','fechaInicio','fechaFin','nombreFicheroCenso','nombreVotacion',
                'esPresencial','votoRectificable','tipoVotacion','maxElector','enunciado','opciones']

    def clean(self):
        inicio=self.cleaned_data['fechaInicio']
        fin=self.cleaned_data['fechaFin']

        if inicio.strftime('%Y-%m-%d %H:%M:%S')<=datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            raise ValidationError('La fecha ser mayor que la actual.')

        if inicio.strftime('%Y-%m-%d %H:%M:%S')>=fin.strftime('%Y-%m-%d %H:%M:%S'):
            raise ValidationError('La fecha de Fin debe ser mayor a la de Inicio.')    

        return self.cleaned_data        
    

class favor(forms.ModelForm):
     vF= forms.CharField(label='aFavor', max_length=1)
	class Meta:
	  model=vF;
	  fields=['aFavor']
			def clean(self):
			  self.cleaned_data['aFavor']
		
		

class contr(forms.ModelForm):
    vC= forms.CharField(label='enContra', max_length=1)
		class Meta:
		   model=vC
		   fields=['enContra']
			def clean(self):
			  self.cleaned_data['enContra']
		

class abst(forms.ModelForm):
    vA= forms.CharField(label='abstencion', max_length=1)
		class Meta:
		 model=vA;
		 fields=['abstencion']
			def clean(self):
			  self.cleaned_data['abstencion']
