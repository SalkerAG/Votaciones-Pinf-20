from django.urls import reverse
from django.views.generic import TemplateView, FormView, CreateView
from django.views.generic.list import ListView
from .models import ProcesoElectoral, Opciones, Pregunta, Votacion, Eleccion
from .forms import VotacioneForm
from django.shortcuts import render, redirect
import datetime


class CrearVotacionView(CreateView):
    model = Votacion
    template_name = 'CrearVotacion.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('listavotaciones')

    # def get(self, request):
    #     form = VotacioneForm()
    #     post = Votacion.objects.all()
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request):
    #     form = VotacioneForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.save()
    #
    #         form = VotacioneForm()
    #         return redirect('')
    #
    #     args = {'form': form}
    #     return render(request, self.template_name, args)


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

class ListaVotacionView(ListView):
    model = Votacion
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.timezone.now()
        return context
