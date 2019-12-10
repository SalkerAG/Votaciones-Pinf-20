from django.contrib import admin
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones

class VotacioneAdmin(admin.TabularInline):
    model = Votacione

class ProcesoElectoralAdmin(admin.ModelAdmin):
    inlines = [VotacioneAdmin,]



# Register your models here.
admin.site.register(Votacione)
admin.site.register(ProcesoElectoral, ProcesoElectoralAdmin)
admin.site.register(Pregunta)
admin.site.register(Eleccion)
admin.site.register(Opciones)