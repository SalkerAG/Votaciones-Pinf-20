from django.shortcuts import render,HttpResponse
from .models import UsuarioUcausuariouca # aqui importamos nuestra tabla a views


def Censo(request): # request este parametro es la peticion que ha pedido el usuario
    usuario = UsuarioUcausuariouca.objects.all() # metemos dichos campos en usuario
    return render(request,"Censo/censo.html", {'usuario': usuario}) # devolvemos los usuarios al template de nuestra tabla

def post(request, id):
    post = Post.objects.get(id = id)
    return render(request, "Censo/censo.html", {'posts': posts})


