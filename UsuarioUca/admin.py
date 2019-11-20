# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserLoginForm
from .models import UsuarioUca, Profesor, PASS, Estudiante
from import_export import resources
import re
from django.forms import ValidationError
import logging

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

logger = logging.getLogger(__name__)


def check(email):
    # pass the regualar expression
    # and the string in search() method
    if re.search(regex, email):
        print("Valid Email")
        return True

    else:
        print("Invalid Email")
        return False


class UsuarioUcaResource(resources.ModelResource):
    class Meta:
        model = UsuarioUca


    def before_import(self, dataset, using_transactions, dry_run, **kwargs):

        for row in dataset:
            email = row[13]
            if check(email) == False:
                raise ValidationError('Email incorrecto. '
                                      'Error en la fila con id = %s' % row[0])


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
