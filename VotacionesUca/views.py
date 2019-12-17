from django.views.generic import TemplateView, FormView
from .models import ProcesoElectoral, Opciones, Pregunta, Votacion, Eleccion
from .forms import VotacioneForm
from django.shortcuts import render, redirect
import datetime


class CrearVotacionView(TemplateView):
    template_name = 'CrearVotacion.html'

    def get(self, request):
        form = VotacioneForm()
        post = Votacion.objects.all()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VotacioneForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            form = VotacioneForm()
            return redirect('/crearVotacion/')

        args = {'form': form}
        return render(request, self.template_name, args)


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
