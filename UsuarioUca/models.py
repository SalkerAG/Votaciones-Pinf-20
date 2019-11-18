# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.forms import forms


def validonif(nif):

    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"
    # nif = nif.upper()
    if len(nif) == 8:
        dig_control = nif[7]
        nif = nif[:7]
        if nif[0] in dig_ext:
            nif = nif.replace(nif[0], reemp_dig_ext[nif[0]])
        return len(nif) == len([n for n in nif if n in numeros]) \

    return False


class UserManager(BaseUserManager):
    def create_user(self, nif, email, first_name, last_name, password, is_staff, is_superuser, is_active):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not nif:
            raise ValueError("User must have a nif")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.nif = nif
        user = self.model(nif=nif, email=email, first_name=first_name, last_name=last_name, is_staff=is_staff,
                          is_superuser=is_superuser, is_active=is_active)
        user.set_password(password)  # change password to hash
        user.save(using=self._db)
        return user

    # def create_user(self, nif, email, first_name="", last_name="", password=None, is_staff=False, is_superuser=False, is_active=False):
    #     is_staff = is_staff
    #     is_superuser = is_superuser
    #     is_active = is_active
    #     return self._create_user(nif, email, first_name, last_name, password, is_staff, is_superuser, is_active)

    def create_superuser(self, nif, email, first_name="", last_name="", password=None, is_staff=True, is_superuser=True, is_active=True):
        is_staff=is_staff
        is_superuser=is_superuser
        is_active=is_active

        return self.create_user(nif, email, first_name, last_name, password, is_staff, is_superuser, is_active)


class UsuarioUca(AbstractUser):
    username = None
    nif = models.CharField(max_length=8, blank=False, null=False, default=32085090, unique=True)
    egresado = models.BooleanField(default=True)
    email = models.EmailField(max_length=64, unique=True)
    USERNAME_FIELD = 'nif'
    REQUIRED_FIELDS = ['email']


    # def clean_fields(self, exclude=None):
    #     nif = self.nif
    #     if validonif(nif) == True:
    #         print(nif)
    #         return nif
    #     else:
    #         raise forms.ValidationError("NIF INCORRECTO")

    objects = UserManager()

    def __str__(self):
        return self.nif


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
