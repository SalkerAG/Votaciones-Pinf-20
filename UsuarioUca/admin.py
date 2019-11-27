# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.validators import RegexValidator
from import_export.admin import ImportExportModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserLoginForm
from .models import UsuarioUca, Profesor, PASS, Estudiante, validonifspain, validonifworld, uvalidonifspain, \
    uvalidonifworld
from import_export import resources, fields
import re
from django.forms import ValidationError
import logging

istextvalidator = RegexValidator("^[a-zA-Z0]*$")

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

logger = logging.getLogger(__name__)


def check(email):
    if re.search(regex, email):
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

    # def before_export(self, queryset, *args, **kwargs):
    #     data = UsuarioUcaResource().export(queryset)
    #     data.csv

    def export(self, queryset=None, *args, **kwargs):
        # for user in queryset:
        #     user.nif = user.nif.replace("u", "")
        # users = UsuarioUca.objects.all()

        qs = list(queryset)
        print(qs)
        for user in qs:
            user.nif = user.nif.replace("u", "")


        return super(UsuarioUcaResource, self).export(qs, *args, **kwargs)

    def before_import(self, dataset, using_transactions, dry_run=True, **kwargs):

        # def replace_row(row_index, row_dict):
        #
        #     del dataset[row_index]
        #     dataset.insert(row_index, row_dict.values())

        for row in dataset:
            email = row[13]
            nif = row[11]
            # nif = "u" + nif
            # row[11] = nif
            # print(nif)
            password = row[1]
            first_name = row[6]
            last_name = row[7]

        if check(email) == False:
            raise ValidationError('Email incorrecto. '
                                  'Error en la fila con nif = %s' % row[11])
        if nif == "":
            raise ValidationError('Nif vacío. '
                                  'Error en la fila con nif = %s' % row[11])
        # if validonifspain(nif) == False and validonifworld(nif) == False:
        #     raise ValidationError('Nif incorrecto. '
        #                           'Error en la fila con nif = %s' % row[11])

        if password == "":
            raise ValidationError('Password vacío. '
                                  'Error en la fila con nif = %s' % row[11])
        if first_name == "":
            raise ValidationError('Nombre vacío. '
                                  'Error en la fila con nif = %s' % row[11])
        if last_name == "":
            raise ValidationError('Apellidos vacío. '
                                  'Error en la fila con nif = %s' % row[11])

        # if is_number(first_name):
        #     raise ValidationError('Nombre incorrecto. '
        #                           'Error en la fila con nif = %s' % row[11])
        # if is_number(last_name):
        #     raise ValidationError('Apellidos incorrecto. '
        #                           'Error en la fila con nif = %s' % row[11])

        # for row_index, row_values in enumerate(dataset):
        #     row = dict(zip(dataset.headers, row_values))
        #     if  row['nif']:
        #
        #         print (nif)
        #     replace_row(row_index, row)
        #
        def replace_row(row_index, row_dict):
            """'pop' for specific index number within dataset, followed by insertion of new 'row' values"""
            del dataset[row_index]
            dataset.insert(row_index, row_dict.values())

        for row_index, row_values in enumerate(dataset):
            row = dict(zip(dataset.headers, row_values))
            if not row['nif'].__contains__("u"):
                row['nif'] = "u" + row['nif']
                replace_row(row_index, row)
        # ds = list(dataset)
        # for row in ds:
        #     row = list(row)
        #
        # print(type(ds[0]))
        # print(ds[0][11])
        # # print (ds[0])
        #
        # for _ in ds:
        #     ds[0][11] = "u" + ds[0][11]


        # # ds[11] = 4
        # for user in ds:
        #     user = list(user)
        #     user[11] = '3'
        #     user = tuple(user)
        #     print (user[11])


        # print(ds)
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

    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ()}),
    #     ('Datos de ingreso', {'fields': ('nif', 'egresado')}),
    # )
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
