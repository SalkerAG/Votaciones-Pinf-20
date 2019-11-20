from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'VotacionesUca/home.html')

def crearVotacion(request):
    return render(request,'VotacionesUca/CrearVotacion.html')

