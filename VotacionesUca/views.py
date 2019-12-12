from django.views.generic.edit import FormView
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones
from .forms import VotacioneForm


class CrearVotacionView(FormView):
	template_name ='CrearVotacion.html'
	success_url='/crearVotacion/'
	form_class=VotacioneForm

	def form_valid(self,form):
		return super().form_valid(form)


	



		
