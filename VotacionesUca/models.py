
from django.db import models
from django.utils import timezone
from django.forms import forms
from enum import Enum

def choices(em):
    return [(e.value, e.name)for e in em]

class tipoV(Enum):
    SIMPLE = 0
    COMPLEJA = 1

class ProcesoElectoral(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    esConsulta = models.BooleanField(default=True)
   # fechaInicio = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
   # fechaFin = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    nombreFicheroCenso = models.TextField

class Pregunta(models.Model):
    enunciado = models.CharField(max_length=50, blank=False, null=False, unique=True)
    opciones = models.TextField

class Votacione(models.Model):
    proceso = models.OneToOneField(ProcesoElectoral, on_delete=models.PROTECT, primary_key=True)
    pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT)
    esPresencial = models.BooleanField(default=False)
    votoRectificable = models.BooleanField(default=False)
    tipoVotacion = models.IntegerField(choices=choices(tipoV), default=tipoV.SIMPLE)
    

class Eleccion(models.Model):
    proceso = models.OneToOneField(ProcesoElectoral, on_delete=models.PROTECT, primary_key=True)
    



