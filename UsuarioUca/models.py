# users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.forms import forms

import csv

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# used to map csv headers to location fields
HEADERS = {
    'id': {'field': 'id', 'required': True},
    'password': {'field': 'password', 'required': True},
}


def import_document_validator(document):
    # check file valid csv format
    try:
        dialect = csv.Sniffer().sniff(document.read(1024))
        document.seek(0, 0)
    except csv.Error:
        raise ValidationError(u'Not a valid CSV file')
    reader = csv.reader(document.read().splitlines(), dialect)
    csv_headers = []
    required_headers = [header_name for header_name, values in
                        HEADERS.items() if values['required']]
    for y_index, row in enumerate(reader):
        # check that all headers are present
        if y_index == 0:
            # store header_names to sanity check required cells later
            csv_headers = [header_name.lower() for header_name in row if header_name]
            missing_headers = set(required_headers) - set([r.lower() for r in row])
            if missing_headers:
                missing_headers_str = ', '.join(missing_headers)
                raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
            continue
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            continue
        # sanity check required cell values
        for x_index, cell_value in enumerate(row):
            # if indexerror, probably an empty cell past the headers col count
            try:
                csv_headers[x_index]
            except IndexError:
                continue
            if csv_headers[x_index] in required_headers:
                if not cell_value:
                    raise ValidationError(u'Missing required value %s for row %s' %
                                          (csv_headers[x_index], y_index + 1))
    return True


class Import(models.Model):
    imported = models.BooleanField(default=False)
    name = models.CharField(primary_key=True, max_length=255)
    document = models.FileField(upload_to='imports', validators=[import_document_validator])
    import_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.name


def validonif(nif):
    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"
    nif = nif.upper()
    if len(nif) == 9:
        dig_control = nif[8]
        nif = nif[:8]
        if nif[0] in dig_ext:
            nif = nif.replace(nif[0], reemp_dig_ext[nif[0]])
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
    nif = models.CharField(max_length=10, blank=False, null=False, default=320850900, unique=True)
    egresado = models.BooleanField(default=True)
    email = models.EmailField(max_length=64, unique=True)
    USERNAME_FIELD = 'nif'
    REQUIRED_FIELDS = ['email']

    def clean_fields(self, exclude=None):
        nif = self.nif
        if validonif(nif) == True:
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
