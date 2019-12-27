from django.db import models, transaction
from django.db.models import Count
from django.forms import forms
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime

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
    @property
    def votacion_cerrada(self):
        return (self.fecha_fin.strftime('%Y-%m-%d') > datetime.now().strftime('%Y-%m-%d')) or (self.fecha_fin.strftime('%Y-%m-%d') == (datetime.now().strftime('%Y-%m-%d')) and (self.hora_fin.strftime('%H:%M') < datetime.now().strftime('%H:%M')))

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

    Votacion = models.OneToOneField(Votacion, on_delete=models.CASCADE)
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

class OpcionesCompleja(models.Model):
    Pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    # enunciado = models.CharField(max_length=50)
    respuesta = models.CharField(max_length=50)

    def __unicode__(self):
        return self.respuesta


class UsuarioVotacion(models.Model):
    # RESPUESTA_CHOICES = (
    #     ("SI", "SI"),
    #     ("NO", "NO"),
    #     ("ABSTENCIÓN", "ABSTENCIÓN"),
    # )

    user = models.ForeignKey(UsuarioUca, on_delete=models.PROTECT, null=True)

    Votacion = models.ForeignKey(Votacion, on_delete=models.PROTECT)

    Pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT)

    seleccion = models.CharField(max_length=20, null=True)

    # opcionesCompleja = models.ForeignKey(OpcionesCompleja, on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('home')

    def save(self, *args, **kwargs):
        super(UsuarioVotacion, self).save(*args, **kwargs)
        for row in UsuarioVotacion.objects.all():
            if UsuarioVotacion.objects.filter(
                    Votacion_id=row.Votacion_id).count() > 1 and UsuarioVotacion.objects.filter(
                Pregunta_id=row.Pregunta_id).count() > 1 and UsuarioVotacion.objects.filter(
                user_id=row.user_id).count() > 1:
                row.delete()




class Eleccion(ProcesoElectoral):
    nombre = models.CharField(max_length=50)
    TIPO_ELECCION = (
        ("0", "Grupos"),
        ("1", "Unipersonales"),
    )
    tipo_eleccion = models.CharField(max_length=10, choices=TIPO_ELECCION, default="Simple")
    max_candidatos = models.IntegerField(default=2, validators=[MinValueValidator(2)])
    max_vacantes = models.FloatField(null=True, default=0.7, validators=[MinValueValidator(0.1), MaxValueValidator(0.99)])

    def __str__(self):
        return self.nombre


class Personas(models.Model):
    Eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    def clean_fields(self, exclude=None):
        # for row in Personas.objects.all():
        maxcandidatos = self.Eleccion.max_candidatos
        if Personas.objects.filter(Eleccion_id=self.Eleccion_id).count() > maxcandidatos - 1:
            raise forms.ValidationError("Ha superado el numero de candidatos máximos")
        else:
            return super(Personas, self).save()

        # super(Personas, self).save(*args, **kwargs)


# for row in UsuarioVotacion.objects.all():
#          if UsuarioVotacion.objects.filter(
#                  Votacion_id=row.Votacion_id).count() > 1 and UsuarioVotacion.objects.filter(
#              Pregunta_id=row.Pregunta_id).count() > 1 and UsuarioVotacion.objects.filter(
#              user_id=row.user_id).count() > 1:
#              row.delete()
#
#      return super(UsuarioVotacion, self).save(*args, **kwargs)

# class Grupos(models.Model):
#     Eleccion = models.ForeignKey(Eleccion, on_delete=models.PROTECT)
#
#     nombre = models.CharField(max_length=20, unique=True)
#
#     def clean_fields(self, exclude=None):
#         # for row in Personas.objects.all():
#
#         maxcandidatos = self.Eleccion.max_candidatos
#         print(maxcandidatos)
#         if Grupos.objects.filter(Eleccion_id=self.Eleccion_id).count() > maxcandidatos - 1:
#             raise forms.ValidationError("Ha superado el numero de candidatos máximos")
#         else:
#             return super(Grupos, self).save()


class UsuarioEleccion(models.Model):
    user = models.ForeignKey(UsuarioUca, on_delete=models.PROTECT, null=True)

    Eleccion = models.ForeignKey(Eleccion, on_delete=models.PROTECT, null=True)

    seleccion = models.CharField(max_length=20, null=True)

    # grupos = models.ManyToManyField(Personas, blank=False)

    def save(self, exclude=None):

        maxcandidatos = self.Eleccion.max_candidatos
        maxvacantes = self.Eleccion.max_vacantes
        for row in UsuarioEleccion.objects.all():
            if self.Eleccion.tipo_eleccion == '0':

                res = int (maxvacantes * maxcandidatos)
                print (res)
                contador =  (UsuarioEleccion.objects.filter(Eleccion_id = self.Eleccion_id).count())
                if contador > res:
                    raise ValueError("Ha superado el numero de candidatos máximos")

                else:
                    return super(UsuarioEleccion, self).save(*args, **kwargs)




class Censo(models.Model):
    usuario = models.ManyToManyField(UsuarioUca, blank=False)
    pregunta = models.OneToOneField(Pregunta, on_delete=models.CASCADE, null=True, blank=True)
    eleccion = models.OneToOneField(Eleccion, on_delete=models.CASCADE, null=True, blank=True)
