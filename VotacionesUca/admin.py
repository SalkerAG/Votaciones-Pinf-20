from django.contrib import admin
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion

# Register your models here.
admin.site.register(Votacione)
admin.site.register(ProcesoElectoral)
admin.site.register(Pregunta)