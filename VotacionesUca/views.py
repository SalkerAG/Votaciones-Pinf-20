from django.views.generic.base import TemplateView
from .models import ProcesoElectoral, Pregunta, Votacione, Eleccion, Opciones

<<<<<<< Updated upstream
class CrearVotacionView(TemplateView):
    template_name = "CrearVotacion.html"
=======
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Votacione,Pregunta,ProcesoElectoral,Opciones
from .forms import VotacioneForm

def VotacioneView(request):
    form=VotacioneForm()
    return render(request, 'VotacionesUca/CrearVotacion.html', {'form':form})
>>>>>>> Stashed changes
