from django.views.generic.base import TemplateView
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones

class CrearVotacionView(TemplateView):
    template_name = "CrearVotacion.html"
    return
