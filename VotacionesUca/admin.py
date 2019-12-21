from django.contrib import admin
from .models import Votacion, ProcesoElectoral, Eleccion, Pregunta

admin.site.register(Votacion)
admin.site.register(ProcesoElectoral)
admin.site.register(Eleccion)
admin.site.register(Pregunta)
# admin.site.register(Opciones)