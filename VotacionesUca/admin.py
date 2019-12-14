from django.contrib import admin
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones

class VotacioneAdmin(admin.TabularInline):
    model = Votacione

class ProcesoElectoralAdmin(admin.ModelAdmin):
    inlines = [VotacioneAdmin,]

admin.site.register(Votacione)