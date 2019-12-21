from time import timezone

from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, FormView, CreateView, DetailView
from django.views.generic.list import ListView
from import_export import resources

from UsuarioUca.admin import UsuarioUcaResource
from UsuarioUca.import_export_views import ImportView
from UsuarioUca.models import UsuarioUca
from VotacionesUca.admin import CensoResource
from .models import ProcesoElectoral, Pregunta, Votacion, Eleccion, OpcionesSimple, OpcionesCompleja, Censo
from .forms import VotacionForm, PreguntaForm, OpcionesComplejaForm, createCensoForm
from django.shortcuts import render, redirect
import datetime
import csv



class CrearCensoView(CreateView):
    model = Censo
    form_class = createCensoForm

    def get_success_url(self):
        return reverse('censo-detail', kwargs={"pk": self.object.pk})


class CensoDetailView(DetailView):
    model = Censo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['users'] = self.object.usuario.all
        return context


class CensoExportView(ImportView, resources.ModelResource):
    class Meta:
        model = UsuarioUca

    def get(self, queryset, *args, **kwargs):
        censo_id = kwargs.pop("pk")
        censo = Censo.objects.get(id=censo_id)
        users_censo = censo.usuario.all()
        for user in users_censo:
            user.nif = user.nif.replace("u", "")
            user.nif = user.nif[:2] + "***" + user.nif[5:]
        output = []
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Censo' + str(censo_id) + '.csv'
        writer = csv.writer(response)
        query_set = users_censo
        writer.writerow(['Nif'])
        for user in query_set:
            output.append([user])
        # CSV Data
        writer.writerows(output)
        return response
        # dataset = CensoResource().export(queryset)
        # response = HttpResponse(dataset.csv, content_type="csv")
        # response['Content-Disposition'] = 'attachment; filename=Censo' + str(censo_id) + '.csv'
        # return response


class CrearVotacionView(CreateView):
    model = Votacion
    form_class = VotacionForm

    # def get_success_url(self):
    #     if self.object.tipo_votacion == 0:
    #         return reverse('crearpreguntasimple')
    #
    #     if self.object.tipo_votacion == 1:
    #         return reverse('crearpreguntacompleja')
    def get_success_url(self):
        return reverse('crearpregunta')


class CrearPregunta(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'CrearPregunta.html'

    def get_success_url(self):
        if self.object.tipo_votacion == "0":
            return reverse('crearpreguntasimple')
        else:
            return reverse('crearpreguntacompleja')


class CrearPreguntaComplejaView(CreateView):
    model = OpcionesCompleja
    form_class = OpcionesComplejaForm
    template_name = 'CrearVotacionCompleja.html'
    success_url = '/crearpreguntacompleja'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.POST = None
        self.method = None

    def index(self):
        form = OpcionesComplejaForm()
        return render(self, 'home.html', {'form': form, })


class CrearPreguntaSimpleView(CreateView):
    model = OpcionesSimple
    fields = '__all__'
    template_name = 'CrearVotacionSimple.html'

    def get_succes_url(self):
        return reverse('/')


class VotacionView(DetailView):
    model = Votacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pregunta = Pregunta.objects.get(votacion=self.object.id)
        context['now'] = datetime.datetime.now()
        context['opciones'] = Opciones.objects.filter(pregunta=pregunta.pk)
        return context


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
