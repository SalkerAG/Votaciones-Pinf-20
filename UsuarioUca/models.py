# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class UsuarioUca(AbstractUser):
    dni = models.CharField(max_length=9, blank=False, null=False, default="00000000A")
    egresado = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class PASS(models.Model):
    class Meta:
        verbose_name_plural = "Pass"

    user = models.OneToOneField(UsuarioUca, on_delete=models.PROTECT, primary_key=True)


class Estudiante(models.Model):
    user = models.OneToOneField(UsuarioUca, on_delete=models.PROTECT, primary_key=True)
    curso_max = models.IntegerField(blank=False, null=False)


class Profesor(models.Model):
    class Meta:
        verbose_name_plural = "Profesores"

    user = models.OneToOneField(UsuarioUca, on_delete=models.PROTECT, primary_key=True)
    permanente = models.BooleanField(default=False)
    doctor = models.BooleanField(default=False)
