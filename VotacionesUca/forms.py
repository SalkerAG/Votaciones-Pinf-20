#users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral,Opciones,Pregunta, Votacion, Eleccion
  
c=[('0','Simple'),('1','Compleja')]
b=[('0','No'),('1','Sí')]

class ProcesoElectoralForm(forms.ModelForm):
    fecha_inicio=forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control inputstl', 'placeholder':'Select Date'},format='%Y/%m/%d'))
    fecha_fin=forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form-control inputstl', 'placeholder':'Select Date'},format='%Y/%m/%d'))
    #hora_inicio = forms.TimeField()
    #hora_fin = forms.TimeField()
    es_consulta=forms.BooleanField(required=False)
    hora_inicio=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time', 'class':'form-control inputstl'})  )
    hora_fin=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time', 'class':'form-control inputstl'}) )
    #esConsulta=forms.ChoiceField(widget=forms.Select(), choices=b)
    #fecha_inicio = forms.DateField()
    #fecha_fin = forms.DateField()
    #nombreFicheroCenso=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Nombre del Censo'}),required=True)
    
    class Meta:
        model=ProcesoElectoral
        fields='__all__'

class PreguntaForm(forms.ModelForm):
    enunciado=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Pregunta para la votacion'}))
    opciones=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Pregunta para la votacion'}))
    class Meta:
        model=Pregunta
        fields = '__all__'

class VotacionForm(ProcesoElectoralForm):
    voto_restringido = forms.BooleanField(required=False)
    nombre_votacion=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Título de la votacion'}), required=True)
    es_presencial=forms.BooleanField(required=False)
    voto_rectificable=forms.BooleanField(required=False)
    tipo_votacion=forms.ChoiceField(choices=c)
    max_respuestas=forms.IntegerField()

    class Meta:
        model=Votacion
        fields= '__all__'

    def clean(self):
        inicio=self.cleaned_data['fecha_inicio']
        fin=self.cleaned_data['fecha_fin']

        if inicio.strftime('%Y-%m-%d')<=datetime.now().strftime('%Y-%m-%d'):
            raise ValidationError('La fecha ser mayor que la actual.')

        if inicio.strftime('%Y-%m-%d')>=fin.strftime('%Y-%m-%d'):
            raise ValidationError('La fecha de Fin debe ser mayor a la de Inicio.')    

        return self.cleaned_data


