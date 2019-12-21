from django.contrib import admin
from django.urls import path, include

from UsuarioUca.views import HomeView
from .views import CrearVotacionView, VotacionView, VotacionComplejaView, CrearPreguntaComplejaView, \
    CrearPreguntaSimpleView, CrearPregunta

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacion"),
    path('crearpreguntacompleja/', CrearPreguntaComplejaView.as_view(), name="crearpreguntacompleja"),
    path('crearpreguntasimple/', CrearPreguntaSimpleView.as_view(), name="crearpreguntasimple"),
    path('crearpregunta/', CrearPregunta.as_view(), name="crearpregunta"),
    path('', HomeView.as_view(), name="home"),
    # path('votacionCompleja/', VotacionComplejaView.as_view(), name="votacioncompleja")
]


# def index(request):
#     if request.method == 'POST':
#         form = OpcionesComplejaForm(request.POST)
#         if form.is_valid():
#             Respuesta_elegida = form.cleaned_data.get('Respuesta_elegida', [])
#             Otra_Respuesta = form.cleaned_data.get('other_book_name', '')
#             OpcionesCompleja.bulk_vote(Respuesta_elegida + [Otra_Respuesta])
#         message = 'Thank You For Your Contribution!'
#     elif request.method == 'GET':
#         message = ''
#
#     form = OpcionesComplejaForm()
#     return render(request, 'home', {'form': form, 'message': message})