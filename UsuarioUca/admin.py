# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import check_password, identify_hasher, is_password_usable
from django.core.validators import RegexValidator
from import_export.admin import ImportExportModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserLoginForm
from .models import UsuarioUca, Profesor, PASS, Estudiante, validonifspain, validonifworld, uvalidonifspain, \
    uvalidonifworld
from import_export import resources, fields
import re
from django.forms import ValidationError




# regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
regex = '^\w+([\.-]?\w+)*@alum.uca.es'
regexname = "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*"

passwordtemplate = "pbkdf2_sha256"




def check(self):
    if re.search(regex, self):
        return True

    else:
        return False


def checkname(self):
    if re.search(regexname, self):
        return True

    else:
        return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False





class UsuarioUcaResource(resources.ModelResource):
    class Meta:
        model = UsuarioUca

    def export(self, queryset=None, *args, **kwargs):

        qs = list(queryset)
        print(qs)
        for user in qs:
            user.nif = user.nif.replace("u", "")

        return super(UsuarioUcaResource, self).export(qs, *args, **kwargs)

    def before_import(self, dataset, using_transactions, dry_run=True, **kwargs):

        for row in dataset:
            email = row[13]
            nif = row[11]
            password = row[1]
            first_name = row[9]
            last_name = row[10]
            is_staff = row[6]
            is_active = row[7]
            print (identify_hasher(password))
            print (identify_hasher(passwordtemplate))


            if check(email) == False:
                raise ValidationError('Email incorrecto. '
                                      'Error en la fila con nif = %s' % row[11])
            if nif == "":
                raise ValidationError('Nif vacío. '
                                      'Error en la fila con nif = %s' % row[11])

            if validonifspain(nif) == False and validonifworld(nif) == False:
                raise ValidationError('Nif incorrecto. '
                                      'Error en la fila con nif = %s' % row[11])

            if checkname(first_name) == False:
                raise ValidationError('Nombre incorrecto. '
                                      'Error en la fila con nif = %s' % row[11])

            if checkname(last_name) == False:
                raise ValidationError('Nombre incorrecto. '
                                      'Error en la fila con nif = %s' % row[11])


            if not identify_hasher(password) == identify_hasher(passwordtemplate):
                raise ValidationError('Contraseña no valida. '
                                      'Error en la fila con nif = %s' % row[11])

            if first_name == "":
                raise ValidationError('Nombre vacío. '
                                      'Error en la fila con nif = %s' % row[11])
            if last_name == "":
                raise ValidationError('Apellidos vacío. '
                                      'Error en la fila con nif = %s' % row[11])
            if len(first_name) < 3:
                raise ValidationError('Nombre debe tener 3 letras mínimo. '
                                      'Error en la fila con nif = %s' % row[11])
            if len(last_name) < 3:
                raise ValidationError('Apellidos debe tener 3 letras mínimo. '
                                      'Error en la fila con nif = %s' % row[11])
            if int(is_active) < 0 or int(is_active) > 1:
                raise ValidationError('Distinto de 0 o 1. '
                                      'Error en la fila con nif = %s' % row[11])
            if int(is_staff) < 0 or int(is_staff) > 1:
                raise ValidationError('Distinto de 0 o 1. '
                                      'Error en la fila con nif = %s' % row[11])


            def replace_row(row_index, row_dict):
                """'pop' for specific index number within dataset, followed by insertion of new 'row' values"""
                del dataset[row_index]
                dataset.insert(row_index, row_dict.values())

            for row_index, row_values in enumerate(dataset):
                row = dict(zip(dataset.headers, row_values))
                if not row['nif'].__contains__("u"):
                    row['nif'] = "u" + row['nif']
                    replace_row(row_index, row)
            return super(UsuarioUcaResource, self).before_import(dataset, using_transactions, dry_run=True, **kwargs)


class UsuarioUcaAdmin(ImportExportModelAdmin, UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    resource_class = UsuarioUcaResource
    model = UsuarioUca
    ordering = ('last_name',)
    fieldsets = (
        ('Informacion personal', {'fields': ('nif', 'first_name', 'last_name', 'email', 'password', 'egresado')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("nif", "email", "password1", "password2", "first_name", "last_name"),
            },
        ),
    )
    list_display = ('nif', 'first_name', 'last_name', 'email')


class EstudianteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'curso_max')


class PASSAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user',)


class ProfesorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'permanente', 'doctor')


admin.site.register(UsuarioUca, UsuarioUcaAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(PASS, PASSAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
