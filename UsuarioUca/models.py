# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class UsuarioUca(AbstractUser):
    dni = models.CharField(max_length=9, blank=False, null=False)
    egresado = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class PASS(models.Model):
    class Meta:
        verbose_name_plural = "Pass"

    user = models.OneToOneField(UsuarioUca, on_delete=models.PROTECT, primary_key=True)


class Estudiante(models.Model):

    user = models.OneToOneField(UsuarioUca, on_delete=models.PROTECT, primary_key=True)
    curso_max = models.IntegerField(blank=False, null=False, default=1, choices=list(zip(range(1, 5), range(1, 5))))


class Profesor(models.Model):
    class Meta:
        verbose_name_plural = "Profesores"

    user = models.OneToOneField(UsuarioUca, on_delete=models.PROTECT, primary_key=True)
    permanente = models.BooleanField(default=False)
    doctor = models.BooleanField(default=False)
