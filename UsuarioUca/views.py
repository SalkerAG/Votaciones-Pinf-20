from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from import_export.formats import base_formats


from UsuarioUca.admin import UsuarioUcaResource
from UsuarioUca.forms import createUserForm, editUserForm
from UsuarioUca.import_export_views import ImportView
from UsuarioUca.models import UsuarioUca, Estudiante, Profesor, PASS
from import_export import resources, fields
from django.contrib import messages

from VotacionesUca.models import Votacion, Eleccion, Censo


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


class UsuarioUcaListView(LoginRequiredMixin, ListView):
    model = UsuarioUca
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UsuarioUcaUpdate(LoginRequiredMixin, UpdateView):
    model = UsuarioUca

    form_class = editUserForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('usuariouca_list', )


class UsuarioUcaCreate(LoginRequiredMixin, CreateView):
    model = UsuarioUca
    form_class = createUserForm

    def get_success_url(self):
        if self.object.rol == "Estudiante":
            return reverse('estudiante_create')
        if self.object.rol == "Profesor":
            return reverse('profesor_create')
        if self.object.rol == "PASS":
            return reverse('pass_create')


class EstudianteCreate(LoginRequiredMixin, CreateView):
    model = Estudiante
    fields = '__all__'

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})


class ProfesorCreate(LoginRequiredMixin,CreateView):
    model = Profesor
    fields = '__all__'

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})


class PASSCreate(LoginRequiredMixin, CreateView):
    model = PASS
    fields = '__all__'

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})


class UsuarioUcaExportView(LoginRequiredMixin, ImportView, resources.ModelResource):
    class Meta:
        model = UsuarioUca

    def get(self, queryset, *args, **kwargs):
        queryset = UsuarioUca.objects.all()
        dataset = UsuarioUcaResource().export(queryset)
        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = 'attachment; filename=UsuariosUCA' + datetime.now().__str__() + '.csv'
        return response


class MyModelImportView(LoginRequiredMixin, ImportView):
    model = UsuarioUca
    template_name = 'usuariouca_upload.html'
    formats = (base_formats.CSV,)
    resource_class = UsuarioUcaResource

    def get_success_url(self):
        return reverse('usuariouca_list')

    def create_dataset(self, *args, **kwargs):
        """ Insert an extra 'source_user' field into the data.
        """
        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.id] * length,
                           header="source_user")
        return dataset

class VotacionView(LoginRequiredMixin, DetailView):
    model = Votacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pregunta = Pregunta.objects.get(votacion=self.object.id)
        context['now'] = datetime.datetime.now()
        context['opciones'] = Opciones.objects.filter(pregunta=pregunta.pk)
        return context

class HomeView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    context_object_name = 'votacion_list'
    model = Votacion

    def get_context_data(self, **kwargs):
        censos_id = Censo.objects.filter(usuario=self.request.user).values_list('eleccion_id', flat=True)
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'eleccion_list': Eleccion.objects.filter(id__in=censos_id),
            'more_context': Eleccion.objects.filter(id__in=censos_id),
        })
        return context

    def get_queryset(self):
        censos_id = Censo.objects.filter(usuario=self.request.user).values_list('votacion_id', flat=True)
        return Votacion.objects.filter(id__in=censos_id)
    

class CrearVotacionView(LoginRequiredMixin, TemplateView):
    template_name = "CrearVotacion.html"


class FAQView(LoginRequiredMixin, TemplateView):
    template_name = "faq2.0.html"


class EstadisticasVotacionSimpleView(LoginRequiredMixin, TemplateView):
    template_name = "votacionSimpleResultados.html"


class EstadisticasEleccionView(LoginRequiredMixin, TemplateView):
    template_name = "votacionEleccionesResultado.html"


def logout_request(request):
    logout(request)
    return redirect('home')


def erase_request(request, pk):
    UsuarioUca.objects.filter(id=pk).delete()
    return redirect('usuariouca_list')
