from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request,'VotacionesUca/home.html')

def crearVotacion(request):
    return render(request,'VotacionesUca/CrearVotacion.html')
