from django.db import models
from django.utils import timezone
from django.forms import forms
from enum import Enum
from datetime import datetime
from django.forms import ModelForm
from .myfields import EuDateField

def choices(em):
    return [(e.value, e.name)for e in em]

class tipoV(Enum):
    SIMPLE = 0
    COMPLEJA = 1

class ProcesoElectoral(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    esConsulta = models.BooleanField(verbose_name='Consulta')
    fechaInicio=EuDateField('Fecha Inicio:', null=True, blank=True, help_text="")
    fechaFin=EuDateField('Fecha Fin:', null=True, blank=True, help_text="")
    nombreFicheroCenso = models.TextField(null=True)
    class Meta:
        abstract=True
        verbose_name='Proceso Electoral'
        verbose_name_plural='Procesos Electorales'
    def _str_(self):
        return self.nombreFicheroCenso

class Opciones(models.Model):
    opciones = models.CharField(max_length=50,null=False, unique=True)
    class Meta:
        abstract=True
        verbose_name='Opción'
        verbose_name_plural='Opciones'
    def __str__(self):
         return self.nombre

class Pregunta(Opciones):
    enunciado = models.CharField(max_length=50, null=False, unique=True)
    class Meta:
        abstract=True
        verbose_name='Pregunta'
        verbose_name_plural='Preguntas'
    def __str__(self):
        return self.enunciado

class Votacione(ProcesoElectoral,Pregunta):
    nombreVotacion = models.CharField(unique=True, max_length=50, null=False)
    esPresencial  = models.BooleanField(verbose_name='Presencial')
    votoRectificable = models.BooleanField(verbose_name='Habilitar voto rectificable')
    tipoVotacion = models.IntegerField(choices=choices(tipoV), default=tipoV.SIMPLE)
    maxElector = models.IntegerField(verbose_name='Número máximo de respuestas', default=1)
    pregunta=Pregunta()
    class Meta:
        verbose_name='Votación'
        verbose_name_plural='Votaciones'

class Eleccion(ProcesoElectoral):
    maxVacantes = models.FloatField(default=0.7, verbose_name='Número máximo de electores')
    tipoEleccion = models.IntegerField(choices=choices(tipoV), default=tipoV.SIMPLE)
    class Meta:
        verbose_name='Elección'
        verbose_name_plural='Elecciones'