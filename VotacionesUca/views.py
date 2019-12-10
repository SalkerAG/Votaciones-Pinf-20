from django.views.generic import ListView
from django.views.generic.edit import CreateView

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Votacione,Pregunta,ProcesoElectoral
from .forms import VotacioneForm

def VotacioneView(request):
    form=VotacioneForm()
    return render(request, 'VotacionesUca/CrearVotacion.html', {'form':form})