# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UsuarioUca, Profesor, PASS, Estudiante


class UsuarioUcaAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'dni')}
         ),)


admin.site.register(UsuarioUca, UsuarioUcaAdmin)
admin.site.register(Profesor)
admin.site.register(PASS)
admin.site.register(Estudiante)



