from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones
from .forms import VotacioneForm



class CrearVotacionView(FormView):
    template_name = 'CrearVotacion.html'
    success_url = '/crearVotacion/'
    form_class = VotacioneForm

    def form_valid(self, form):
        return super().form_valid(form)


class VotacionSimpleView(FormView):
    template_name = 'VotacionSimple.html'
    success_url = '/votacionSimple/'
    form_class = VotacioneForm

    def form_valid(self, form):
        return super().form_valid(form)


class VotacionComplejaView(FormView):
    template_name = 'VotacionCompleja.html'
    success_url = '/votacionCompleja/'
    form_class = VotacioneForm

    def form_valid(self, form):
        return super().form_valid(form)
