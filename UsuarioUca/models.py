# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.forms import forms

import csv

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

istextvalidator = RegexValidator("^[a-zA-Z0]*$",
                                     message='El Nombre no debe contener números',
                                     code='Nombre invalido')


def uvalidonifworld(nif):
    dig_ext = "uXYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2', 'u': '3'}
    numeros = "1234567890"

    if len(nif) == 10:
        dig_control = nif[9]
        nif = nif[:9]
        if nif[0] in dig_ext:
            nif = nif.replace(nif[0], reemp_dig_ext[nif[0]])
            nif = nif.replace(nif[1], reemp_dig_ext[nif[1]])
        return len(nif) == len([n for n in nif if n in numeros]) \

    return False

def uvalidonifspain(nif):
    dig_ext = "u"
    reemp_dig_ext = {'u': '0'}
    numeros = "1234567890"

    if len(nif) == 9:
        dig_control = nif[8]
        nif = nif[:8]
        if nif[0] in dig_ext:
            nif = nif.replace(nif[0], reemp_dig_ext[nif[0]])

        return len(nif) == len([n for n in nif if n in numeros]) \

    return False

def validonifworld(nif):
    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"

    if len(nif) == 9:
        dig_control = nif[8]
        nif = nif[:8]
        if nif[0] in dig_ext:
            nif = nif.replace(nif[0], reemp_dig_ext[nif[0]])
        return len(nif) == len([n for n in nif if n in numeros]) \

    return False

def validonifspain(nif):

    numeros = "1234567890"

    if len(nif) == 8:
        dig_control = nif[7]
        nif = nif[:7]


        return len(nif) == len([n for n in nif if n in numeros]) \

    return False


class UserManager(BaseUserManager):
    def _create_user(self, nif, email, first_name, last_name, password, is_staff, is_superuser, is_active):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not nif:
            raise ValueError("User must have a nif")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.nif = nif.replace(nif, "u" + nif)
        user = self.model(nif=user.nif, email=email, first_name=first_name, last_name=last_name, is_staff=is_staff,
                          is_superuser=is_superuser, is_active=is_active)
        user.set_password(password)  # change password to hash
        user.save(using=self._db)
        return user

    def create_user(self, nif, email, first_name="", last_name="", password=None, is_staff=True, is_superuser=False,
                    is_active=True):
        is_staff = is_staff
        is_superuser = is_superuser
        is_active = is_active
        nif = nif.replace(nif, "u" + nif)
        return self._create_user(nif, email, first_name, last_name, password, is_staff, is_superuser, is_active)

    def create_superuser(self, nif, email, first_name="", last_name="", password=None, is_staff=True, is_superuser=True,
                         is_active=True):
        is_staff = is_staff
        is_superuser = is_superuser
        is_active = is_active

        return self._create_user(nif, email, first_name, last_name, password, is_staff, is_superuser, is_active)


class UsuarioUca(AbstractUser):

    username = None
    #default=320850900
    first_name = models.CharField(max_length=20, blank=False, validators=[istextvalidator])
    last_name = models.CharField(max_length=30, blank=False, validators=[istextvalidator])
    nif = models.CharField(max_length=10, blank=False, null=False, unique=True)
    egresado = models.BooleanField(default=True)
    email = models.EmailField(max_length=64, unique=True)
    USERNAME_FIELD = 'nif'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def clean_fields(self, exclude=None):
        nif = self.nif
        if validonifspain(nif) == True or validonifworld(nif) == True:
            print(nif)
            return nif
        else:
            raise forms.ValidationError("NIF INCORRECTO")

    objects = UserManager()

    def __str__(self):
        return str(self.nif)


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
