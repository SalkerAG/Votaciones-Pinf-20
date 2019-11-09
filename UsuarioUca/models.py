# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import forms


def validodni(dni):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
               and tabla[int(dni) % 23] == dig_control
    return False


class UsuarioUca(AbstractUser):
    dni = models.CharField(max_length=9, blank=False, null=False)
    egresado = models.BooleanField(default=True)

    def clean_fields(self, exclude=None):
        dni = self.dni
        if validodni(dni) == True:
            print(dni)
            return dni
        else:
            raise forms.ValidationError("DNI INCORRECTO")

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
