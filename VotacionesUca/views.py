from time import timezone

from django.forms import ModelForm
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.views.generic import TemplateView, FormView, CreateView, DetailView
from django.views.generic.list import ListView
from import_export import resources
from django.http import HttpRequest as request, HttpResponseRedirect
from UsuarioUca.admin import UsuarioUcaResource
from UsuarioUca.import_export_views import ImportView
from UsuarioUca.models import UsuarioUca
from VotacionesUca.admin import CensoResource
from .models import ProcesoElectoral, Pregunta, Votacion, Eleccion, Censo, \
    UsuarioVotacion, OpcionesCompleja
from .forms import VotacionForm, PreguntaForm, createCensoForm, PreguntaFormVotacion, \
    realizarVotacionForm, OpcionesComplejaForm, realizarVotacionComplejaForm
from django.shortcuts import render, redirect
import datetime
import csv
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy


class CrearPreguntaViewCenso(BSModalCreateView):
    form_class = PreguntaForm
    template_name = "CrearPregunta.html"
    success_message = 'Exito: Pregunta creada.'
    success_url = reverse_lazy('censo_create')


class CrearPreguntaViewRealizarVotacion(BSModalCreateView):
    form_class = PreguntaForm
    template_name = "CrearPregunta.html"
    success_message = 'Exito: Pregunta creada.'
    success_url = reverse_lazy('realizarvotacion')


class CrearPreguntaViewVotacion(BSModalCreateView):
    form_class = PreguntaForm
    template_name = "CrearPregunta.html"
    success_message = 'Exito: Pregunta creada.'
    success_url = reverse_lazy('crearvotacion')


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
            user.nif = user.nif[:2] + "*" + user.nif[5:]
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

# class VotacionView(FormMixin, DetailView, request):
#     model = Votacion
#     form_class = realizarVotacionForm
#     template_name = "RealizarVotacion.html"
#     success_url = reverse_lazy('home')
#
#     def get_success_url(self):
#         return reverse('home')
#
#     def get_context_data(self, **kwargs):
#         context = super(VotacionView, self).get_context_data(**kwargs)
#         cosas = self
#         context['form'] = realizarVotacionForm(
#             initial={'user': self.request.user, 'Votacion': self.object, 'Pregunta': self.object.pregunta})
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#
#     def form_valid(self, form):
#         form.save()
#         return super(VotacionView, self).form_valid(form)


class CrearVotacionView(CreateView):
    model = Votacion
    form_class = VotacionForm



    def get_success_url(self):
        return reverse('crearpreguntavotacion')


def load_preguntas(request):
    Votacion_id = request.GET.get('Votacion')
    preguntas = Pregunta.objects.filter(Votacion_id=Votacion_id).order_by('enunciado')
    return render(request, 'preguntas_list_options.html', {'preguntas': preguntas})


class CrearPregunta(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'CrearPregunta.html'

    def get_success_url(self):

        if self.object.tipo_votacion == "0":
            return reverse('home')
        else:
            return reverse('crearpreguntacompleja')

    # def get_context_data(self, **kwargs):
    #     context = super(CrearPregunta, self).get_context_data(**kwargs)
    #     context['form'] = PreguntaForm(
    #         initial={'Votacion': self.object.Votacion, })
    #     return context





class CrearPreguntaVotacion(CreateView):
    model = Pregunta
    form_class = PreguntaFormVotacion
    template_name = "CrearPreguntaVotacion.html"



    def get_success_url(self):
        if self.object.tipo_votacion == '0':
            return reverse('home')
        else:
            return reverse('crearpreguntacompleja')

    # def get_context_data(self, **kwargs):
    #     context = super(CrearPreguntaVotacion, self).get_context_data(**kwargs)
    #     # cosas = self
    #     context['form'] = PreguntaFormVotacion(
    #         initial={'Votacion': self.object.Votacion})
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     p = Pregunta()
    #     p.Votacion = self.object.Votacion
    #     p.enunciado = self.object.enunciado
    #     p.save()
    #     # return HttpResponseRedirect('/')
    #
    # def form_valid(self, form):
    #     form.save()
    #     return super(CrearPreguntaVotacion, self).form_valid(form)


class CrearPreguntaComplejaView(CreateView):
    model = OpcionesCompleja
    form_class = OpcionesComplejaForm
    template_name = 'CrearVotacionCompleja.html'
    success_url = '/crearpreguntacompleja'

    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.POST = None
        self.method = None

    def index(self):
        form = OpcionesComplejaForm()
        return render(self, 'home.html', {'form': form, })

  


# class CrearPreguntaSimpleView(CreateView):
#     model = OpcionesSimple
#     fields = '_all_'
#     template_name = 'CrearVotacionSimple.html'
#
#     def get_succes_url(self):
#         return reverse('/')


class VotacionView(FormMixin, DetailView, request):
    model = Votacion
    form_class = realizarVotacionForm
    template_name = "RealizarVotacion.html"
    success_url = reverse_lazy('home')


    # def add_opcionescomplejas(request):
    #     objectlist = OpcionesCompleja.objects.values('respuesta')
    #     if request.method == 'POST':
    #         form = realizarVotacionForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('home')
    #     else:
    #         form = realizarVotacionForm()
    #     return render(request, 'RealizarVotacion.html', {'form': form, 'objectlist': objectlist})
    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(VotacionView, self).get_context_data(**kwargs)
        cosas = self

        if self.object.pregunta.tipo_votacion == '0':
            context['form'] = realizarVotacionForm(
            initial={'user': self.request.user, 'Votacion': self.object, 'Pregunta': self.object.pregunta})
            return context
        else:
            context['form'] = realizarVotacionComplejaForm(
                initial={'user': self.request.user, 'Votacion': self.object, 'Pregunta': self.object.pregunta})
            return context


    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     usuario_votacion = UsuarioVotacion()
    #     usuario_votacion.seleccion = form.data['seleccion']
    #     usuario_votacion.user = self.request.user
    #     usuario_votacion.Votacion = self.object
    #     usuario_votacion.Pregunta = self.object.pregunta
    #     usuario_votacion.save()
    #     return reverse('home')

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         self.form_valid(form)
    #         return HttpResponseRedirect('home')
    #     else:
    #         self.form_invalid(form)
    #         return HttpResponseRedirect('home')

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form = self.get_form()
        usuario_votacion = UsuarioVotacion()

        usuario_votacion.user = self.request.user
        usuario_votacion.Votacion = self.object
        usuario_votacion.Pregunta = self.object.pregunta
        if usuario_votacion.Pregunta.tipo_votacion == '1':
            usuario_votacion.seleccion = form.data['opcionesCompleja']
        else:
            usuario_votacion.seleccion = form.data['seleccion']
        usuario_votacion.save()
        return HttpResponseRedirect('/')

    def form_valid(self, form):
        form.save()
        return super(VotacionView, self).form_valid(form)



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