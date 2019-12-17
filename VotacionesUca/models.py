from django.db import models

from Censo.models import Censo


class ProcesoElectoral(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    nombre_fichero_censo = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    es_consulta = models.BooleanField(default=False)

class Opciones(models.Model):
    nombre = models.CharField(max_length=50)

class Pregunta(models.Model):
    enunciado = models.CharField(max_length=50)
    opciones = models.ManyToManyField(Opciones)

class Votacion(ProcesoElectoral):
    es_presencial = models.BooleanField(default=False)
    voto_rectificable = models.BooleanField(default=False)
    tipo_votacion = models.BooleanField(default=False)
    max_elector = models.IntegerField()
    pregunta = models.ManyToManyField(Pregunta)

class Eleccion(ProcesoElectoral):
    nie = models.IntegerField()
    max_vacantes = models.IntegerField()
    tipo_eleccion = models.BooleanField(default=False)
    censo = models.OneToOneField(Censo, on_delete=models.CASCADE)





