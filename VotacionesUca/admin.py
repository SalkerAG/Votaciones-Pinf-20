from django.contrib import admin
from import_export import resources

from UsuarioUca.models import UsuarioUca
from .models import Votacion, ProcesoElectoral, Eleccion, Pregunta, Censo

class CensoResource(resources.ModelResource):
    class Meta:
        model = UsuarioUca

    def export(self, queryset=None, *args, **kwargs):

        qs = list(queryset)
        print(qs)


        return super(CensoResource, self).export(qs, *args, **kwargs)



admin.site.register(Votacion)
admin.site.register(ProcesoElectoral)
admin.site.register(Eleccion)
admin.site.register(Pregunta)
admin.site.register(Censo)
# admin.site.register(Opciones)