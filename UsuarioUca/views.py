from django.contrib.auth import authenticate, login
from django.views.generic.base import TemplateView


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


class HomeView(TemplateView):
    template_name = "home.html"


class ListaVotacionesView(TemplateView):
    template_name = "ListaVotaciones.html"


class CrearVotacionView(TemplateView):
    template_name = "CrearVotacion.html"

class FAQView(TemplateView):
    template_name = "faq2.0.html"
