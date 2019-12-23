from django.db import models, transaction
from django.urls import reverse


from django.utils import timezone

from UsuarioUca.models import UsuarioUca

class ProcesoElectoral(models.Model):
    voto_restringido = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    es_consulta = models.BooleanField(default=False)

class Votacion(ProcesoElectoral):
    nombre_votacion = models.CharField(max_length=50, null=True)
    es_presencial = models.BooleanField(default=False)
    voto_rectificable = models.BooleanField(default=False)
    # tipo_votacion = models.BooleanField(default=False)
    # max_respuestas = models.IntegerField()
    # pregunta = models.OneToOneField(Pregunta, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre_votacion

class Opcion(models.Model):
    respuesta = models.CharField(max_length=50)
    def __str__(self):
        return self.respuesta

class Pregunta(models.Model):
    TIPO_CHOICES = (
        ("0", "Simple"),
        ("1", "Compleja"),

    )

    Votacion = models.OneToOneField(Votacion, on_delete=models.PROTECT)
    tipo_votacion = models.CharField(max_length=10, choices=TIPO_CHOICES, default="Simple")
    enunciado = models.CharField(max_length=50)
    # opciones = models.ManyToManyField(Opcion, blank=False)

    def __str__(self):
        return self.enunciado

    
    # curso_max = models.IntegerField(blank=False, null=False, default=1, choices=list(zip(range(1, 5), range(1, 5))))

    # class PreguntaSimple(OpcionesSimple):
    #
    # def get_absolute_url(self):
    #     return reverse('crearpreguntasimple')


class Censo(models.Model):
    usuario = models.ManyToManyField(UsuarioUca, blank=False)
    pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT)





# class OpcionesSimple(models.Model):
#     PREGUNTA_CHOICES = (
#         ("SI", "SI"),
#         ("NO", "NO"),
#         ("ABSTENCIÓN", "ABSTENCIÓN"),
#     )
#
#
#     Pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT, primary_key=True)
#
#     seleccion = models.CharField(max_length=10, choices=PREGUNTA_CHOICES, default="SI")
#
#     def get_absolute_url(self):
#         return reverse('home')


class OpcionesCompleja(models.Model):
    Pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT)
    # enunciado = models.CharField(max_length=50)
    respuesta = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.respuesta

    def __unicode__(self):
        return self.respuesta



class UsuarioVotacion(models.Model):
    # RESPUESTA_CHOICES = (
    #     ("SI", "SI"),
    #     ("NO", "NO"),
    #     ("ABSTENCIÓN", "ABSTENCIÓN"),
    # )

    user = models.ForeignKey(UsuarioUca, on_delete=models.PROTECT, null=True)

    Votacion = models.OneToOneField(Votacion, on_delete=models.PROTECT)

    Pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT, primary_key=True)

    seleccion = models.CharField(max_length=20, null=True)


    opcionesCompleja = models.ForeignKey(OpcionesCompleja, on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('home')




class Eleccion(ProcesoElectoral):
    nie = models.IntegerField()
    max_vacantes = models.IntegerField()
    tipo_eleccion = models.BooleanField(default=False)
    censo = models.OneToOneField(Censo, on_delete=models.CASCADE)
