from django.shortcuts import render

# Create your views here.
def votacionSimple(request):
    return render(request,'VotacionesUca/votacionSimple.html')

def votacionCompleja(request):
    return render(request,'VotacionesUca/votacionCompleja.html')

def elegirVotacion(request):
    return render(request,'VotacionesUca/elegirVotacion.html')