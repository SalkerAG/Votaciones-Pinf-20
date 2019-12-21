from django.contrib import admin
from django.urls import path, include

from UsuarioUca.views import HomeView
from .views import CrearVotacionView, VotacionView, VotacionComplejaView, CrearPreguntaComplejaView, \
    CrearPreguntaSimpleView, CrearPregunta, CrearCensoView, CensoDetailView, CensoExportView, CrearPreguntaView, \
    CrearPreguntaVotacion

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacion"),
    path('crearpreguntacompleja/', CrearPreguntaComplejaView.as_view(), name="crearpreguntacompleja"),
    path('crearpreguntasimple/', CrearPreguntaSimpleView.as_view(), name="crearpreguntasimple"),
    path('crearpreguntavotacion/', CrearPreguntaVotacion.as_view(), name="crearpreguntavotacion"),
    path('crearpregunta/', CrearPregunta.as_view(), name="crearpregunta"),
    path('crearcenso/', CrearCensoView.as_view(), name="censo_create"),
    path('censo/<int:pk>/', CensoDetailView.as_view(), name='censo-detail'),
    path('censo/<int:pk>/export/', CensoExportView.as_view(), name='censo_export'),
    path('preguntacrear/', CrearPreguntaView.as_view(), name='create_pregunta'),
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
