from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_protect
from UsuarioUca.models import UsuarioUca # aqui importamos nuestra tabla a views
from .models import Censo
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy


class CensoCreate(CreateView):
    model = Censo
    fields = ['usuario', 'id_votacion']


class CensoDetailView(CreateView):
    model = Censo
    fields = '__all__'
    success_url = reverse_lazy('admin/')

# def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context


# @csrf_protect
# def Censo(request): # request este parametro es la peticion que ha pedido el usuario
   
#     usuarios = UsuarioUca.objects.all() # metemos dichos campos en usuarios
#     return render(request,"Censo/censo.html", {
#         'usuario': usuarios
#     }) # devolvemos los usuarios al template de nuestra tabla

# def guardarCenso(request, idVotacion):
    
#     # Para obtener los nif de los usuarios que pueden votar en una votacion
#     # usuariosVotacionUca = Censo.objects.get(id_votacion=idVotacion)
    
#     # Para obtener los atributos de los usuarios que pueden votar en una votacion
#     for uvc in usuariosVotacionUca:
#         usuarioUca = UsuarioUca.objects.get(nif = uvc.id_usuario)

#     if request.method=='POST':
#         if request.POST['usuariosVotacion']:
#             for nif in request.POST['usuariosVotacion']:
#                 c = Censo(
#                     id_usuario = nif,
#                     id_votacion = idVotacion
#                 )
#                 c.save()

#     nombre_usuario = ''
    
#     return render(request, "Censo/censo.html", {'posts': []})

