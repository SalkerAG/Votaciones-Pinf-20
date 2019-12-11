from django.views.generic.base import TemplateView
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones


class CrearVotacionView(TemplateView):
    template_name = "CrearVotacion.html"



def votacion(request,op):
	if(op==0):#votacion simple carga vista simple
		template_name = "votacionSimple.html"
	else:
		template_name = "votacionCompleta.html"

	



		
