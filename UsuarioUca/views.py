from datetime import datetime
# from importlib import resources

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from import_export.formats import base_formats
# from sqlalchemy.sql.functions import userdd/

from UsuarioUca.admin import UsuarioUcaResource
from UsuarioUca.forms import createUserForm, editUserForm, createEstudianteForm
from UsuarioUca.import_export_views import ImportView
from UsuarioUca.models import UsuarioUca, Estudiante, Profesor, PASS
from import_export import resources, fields
from django.contrib import messages




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


class UsuarioUcaListView(ListView):
    model = UsuarioUca
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UsuarioUcaUpdate(UpdateView):
    model = UsuarioUca
    # fields = '__all__'
    form_class = editUserForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})


class UsuarioUcaCreate(CreateView):
    model = UsuarioUca
    # fields = '__all__'
    form_class = createUserForm

    def get_success_url(self):
        if self.object.rol == "Estudiante":
            return reverse('profesor_create', kwargs={'user': self.object.nif})
        if self.object.rol == "Profesor":
            return reverse('profesor_create', kwargs={'user': self.object})
        if self.object.rol == "PASS":
            return reverse('pass_create', kwargs={'user': self.object})



class EstudianteCreate(CreateView):

    model = Estudiante
    fields = '__all__'
    slug = None

    def get_object(self, queryset=None):
        return queryset.get(slug= self.slug)
    form_class = createEstudianteForm(initial={'user': get_object()})

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})

class ProfesorCreate(CreateView):
    model = Profesor
    fields = '__all__'

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})

class PASSCreate(CreateView):
    model = PASS
    fields = '__all__'

    def get_success_url(self):
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})


class UsuarioUcaExportView(ImportView, resources.ModelResource):
    class Meta:
        model = UsuarioUca

    def get(self, queryset, *args, **kwargs):
        queryset = UsuarioUca.objects.all()
        dataset = UsuarioUcaResource().export(queryset)
        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = 'attachment; filename=UsuariosUCA' + datetime.now().__str__() + '.csv'
        return response


class MyModelImportView(ImportView):
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


class HomeView(TemplateView):
    template_name = "home.html"


class ListaVotacionesView(TemplateView):
    template_name = "ListaVotaciones.html"


class CrearVotacionView(TemplateView):
    template_name = "CrearVotacion.html"


class FAQView(TemplateView):
    template_name = "faq2.0.html"


class EstadisticasVotacionSimpleView(TemplateView):
    template_name = "votacionSimpleResultados.html"


class EstadisticasEleccionView(TemplateView):
    template_name = "votacionEleccionesResultado.html"


def logout_request(request):
    logout(request)
    messages.info(request, "Se ha cerrado la sesión correctamente")
    return redirect('home')




def erase_request(request, pk):
    UsuarioUca.objects.filter(id=pk).delete()
    return redirect('usuariouca_list')