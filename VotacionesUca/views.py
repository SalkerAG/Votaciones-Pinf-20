from django.urls import reverse
from django.views.generic import TemplateView, FormView, CreateView
from django.views.generic.list import ListView
from .models import ProcesoElectoral, Opciones, Pregunta, Votacion, Eleccion
from .forms import VotacionForm
from django.shortcuts import render, redirect
import datetime


class CrearVotacionView(CreateView):
    model = Votacion
    form_class = VotacionForm
    template_name = 'CrearVotacion.html'

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listavotaciones')


class VotacionSimpleView(FormView):
    template_name = 'VotacionSimple.html'
    success_url = '/votacionSimple/'
    form_class = VotacionForm

    def form_valid(self, form):
        return super().form_valid(form)


class VotacionComplejaView(FormView):
    template_name = 'VotacionCompleja.html'
    success_url = '/votacionCompleja/'
    form_class = VotacionForm

    def form_valid(self, form):
        return super().form_valid(form)

class ListaVotacionView(ListView):
    model = Votacion
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.timezone.now()
        return context
