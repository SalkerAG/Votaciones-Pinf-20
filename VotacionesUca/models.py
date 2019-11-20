
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
    esConsulta = models.BooleanField(default=False, verbose_name='Consulta')
   # fechaInicio CREAR FECHA TIPO DATE_TIME
   # fechaFin CREAR FECHA TIPO DATE_TIME
    nombreFicheroCenso = models.TextField(null=True)
    class Meta:
        verbose_name='Proceso Electoral'
        verbose_name_plural='Procesos Electorales'
    def __str__(self):
        return self.nombreFicheroCenso[0:40]

class Pregunta(models.Model):
    enunciado = models.CharField(max_length=50, null=False, unique=True)
    opciones = models.TextField(null=True)
    class Meta:
        verbose_name='Pregunta'
        verbose_name_plural='Preguntas'
    def __str__(self):
        return self.enunciado[0:40]

class Votacione(models.Model):
    proceso = models.OneToOneField(ProcesoElectoral, on_delete=models.PROTECT, primary_key=True)
    pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT)
    esPresencial = models.BooleanField(default=False, verbose_name='Presencial')
    votoRectificable = models.BooleanField(default=False, verbose_name='Habilitar voto rectificable')
    tipoVotacion = models.IntegerField(choices=choices(tipoV), default=tipoV.SIMPLE)
    class Meta:
        verbose_name='Votación'
        verbose_name_plural='Votaciones'
 #   def __str__(self):
  #      return

class Eleccion(models.Model):
    proceso = models.OneToOneField(ProcesoElectoral, on_delete=models.PROTECT, primary_key=True)
    



