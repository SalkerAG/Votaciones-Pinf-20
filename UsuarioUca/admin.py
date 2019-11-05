# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UsuarioUca, Profesor, PASS, Estudiante


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UsuarioUca
    list_display = ['email', 'username']


admin.site.register(UsuarioUca, CustomUserAdmin)
admin.site.register(Profesor)
admin.site.register(PASS)
admin.site.register(Estudiante)
