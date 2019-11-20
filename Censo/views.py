from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_protect
from UsuarioUca.models import UsuarioUca # aqui importamos nuestra tabla a views
import sys
from random import seed
from random import random
from .models import Censo


@csrf_protect
def Censo(request): # request este parametro es la peticion que ha pedido el usuario
    #seed(1)
    #u = UsuarioUca(
    #    nif = '12345678',
    #    egresado = True,
    #    email = str(random()) + '@gmail.com'
    #)
    #u.save()
    usuarios = UsuarioUca.objects.all() # metemos dichos campos en usuario
    return render(request,"Censo/censo.html", {
        'usuario': usuarios
    }) # devolvemos los usuarios al template de nuestra tabla

def guardarCenso(request, idVotacion):
    
    # Para obtener los nif de los usuarios que pueden votar en una votacion
    # usuariosVotacionUca = Censo.objects.get(id_votacion=idVotacion)
    
    # Para obtener los atributos de los usuarios que pueden votar en una votacion
    for uvc in usuariosVotacionUca:
        usuarioUca = UsuarioUca.objects.get(nif = uvc.id_usuario)

    if request.method=='POST':
        if request.POST['usuariosVotacion']:
            for nif in request.POST['usuariosVotacion']:
                c = Censo(
                    id_usuario = nif,
                    id_votacion = idVotacion
                )
                c.save()

    nombre_usuario = ''
    #print('Value %s' % (nombre_usuario) )
        #for key, value in request.POST.items():
        #    print('Key: %s' % (key) )
        #    print('Value %s' % (value) )
    
    # post = Post.objects.get(id = id)
    
    return render(request, "Censo/censo.html", {'posts': []})


