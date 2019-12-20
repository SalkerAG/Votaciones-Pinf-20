from django.db import models
from django.urls import reverse

from Censo.models import Censo
from django.utils import timezone


class ProcesoElectoral(models.Model):
    voto_restringido = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    es_consulta = models.BooleanField(default=False)

class Opciones(models.Model):
    nombre = models.CharField(max_length=50)

class OpcionesSimple(models.Model):

    PREGUNTA_CHOICES = (
        ("SI", "SI"),
        ("NO", "NO"),
        ("ABSTENCIÓN", "ABSTENCIÓN"),
    )
    seleccion = models.CharField(max_length=10, choices=PREGUNTA_CHOICES, default="SI")

    def get_absolute_url(self):
        return reverse('home')

class Pregunta(OpcionesSimple):
    enunciado = models.CharField(max_length=50)
    # opciones = models.ManyToManyField(OpcionesSimple)

# class PreguntaSimple(OpcionesSimple):


class Votacion(ProcesoElectoral):
    nombre_votacion = models.CharField(max_length=50, null=True)
    es_presencial = models.BooleanField(default=False)
    voto_rectificable = models.BooleanField(default=False)
    tipo_votacion = models.BooleanField(default=False)
    max_respuestas = models.IntegerField()
    pregunta = models.OneToOneField(Pregunta, on_delete=models.CASCADE, null=True, blank=True)
    censo = models.OneToOneField(Censo, on_delete=models.CASCADE, null=True, blank=True)

class Eleccion(ProcesoElectoral):
    nie = models.IntegerField()
    max_vacantes = models.IntegerField()
    tipo_eleccion = models.BooleanField(default=False)
    censo = models.OneToOneField(Censo, on_delete=models.CASCADE, null=True)





