from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView

from UsuarioUca.forms import createUserForm, editUserForm
from UsuarioUca.models import UsuarioUca


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
        return reverse('usuariouca_edit', kwargs={'pk': self.object.pk})


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

class EstadisticasVotacionComplejaView(TemplateView):
    template_name = "votacionComplejaResultados.html"

class EstadisticasEleccionView(TemplateView):
    template_name = "votacionEleccionesResultado.html"
