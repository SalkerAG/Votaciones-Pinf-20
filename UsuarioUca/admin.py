# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import tablib
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, UserLoginForm
from .models import UsuarioUca, Profesor, PASS, Estudiante


class UsuarioUcaAdmin(ImportExportModelAdmin, UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
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
