# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UsuarioUca, Profesor, PASS, Estudiante


class UsuarioUcaAdmin(UserAdmin):
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

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('user', 'curso_max')

class PASSAdmin(admin.ModelAdmin):
    list_display = ('user',)

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('user', 'permanente', 'doctor')

admin.site.register(UsuarioUca, UsuarioUcaAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(PASS, PASSAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
