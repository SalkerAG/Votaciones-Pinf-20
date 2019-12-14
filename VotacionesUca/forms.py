# users/forms.py
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import datetime
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones


def positivo(value):
    if value <= 0:
        raise ValidationError('El número debe ser mayor que 0.')


c = [('0', 'Simple'), ('1', 'Compleja')]


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class ProcesoElectoralForm(forms.ModelForm):
    create_at = forms.DateTimeField()
    update_at = forms.DateTimeField()
    esConsulta = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'customCheck1'}))
    fechaInicio = forms.DateTimeField(label='Fecha Fin del proceso electoralsdsds', required=True, widget=DateTimeInput)
    fechaFin = forms.DateTimeField(label='Fecha Fin del proceso electoral', required=True, widget=DateTimeInput)
    nombreFicheroCenso = forms.CharField(required=True)

    class Meta:
        model = ProcesoElectoral
        fields = '__all__'


class OpcionesForm(forms.ModelForm):
    enunciado = forms.CharField()

    class Meta:
        model = Opciones
        fields = '__all__'


class PreguntaForm(OpcionesForm):
    enunciado = forms.CharField(max_length=50, required=True)
    opciones = OpcionesForm

    class Meta:
        model = Pregunta
        fields = '__all__'


class VotacioneForm(ProcesoElectoralForm, PreguntaForm):
    proceso = ProcesoElectoralForm()
    pregunta = PreguntaForm()
    nombreVotacion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la votación'}))
    esPresencial = forms.BooleanField(label='Proceso Electoral presencial', initial=False)
    votoRectificable = forms.BooleanField(label='Voto rectificable', initial=False)
    tipoVotacion = forms.ChoiceField(label='Tipo de votacion', choices=c)
    maxElector = forms.IntegerField(label='Numero maximo de electores', validators=[positivo], min_value=0)

    class Meta:
        model = Votacione
        fields = '__all__'


class favor(forms.favor):
    vF = forms.CharField(label='aFavor', max_length=1)


class contr(forms.contr):
    vC = forms.CharField(label='enContra', max_length=1)


class abst(forms.abst):
    vA = forms.CharField(label='abstencion', max_length=1)
