from django.contrib import admin
from django.urls import path, include

from UsuarioUca.views import HomeView
from .views import CrearVotacionView, VotacionView, VotacionComplejaView,  \
     CrearPregunta, CrearCensoView, CensoDetailView, CensoExportView, \
    CrearPreguntaVotacion, RealizarVotacion, CrearPreguntaViewCenso, CrearPreguntaViewVotacion, \
    CrearPreguntaViewRealizarVotacion, load_preguntas

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacion"),
    # path('crearpreguntacompleja/', CrearPreguntaComplejaView.as_view(), name="crearpreguntacompleja"),
    # path('crearpreguntasimple/', CrearPreguntaSimpleView.as_view(), name="crearpreguntasimple"),
    path('crearpreguntavotacion/', CrearPreguntaVotacion.as_view(), name="crearpreguntavotacion"),
    path('crearpregunta/', CrearPregunta.as_view(), name="crearpregunta"),
    path('crearcenso/', CrearCensoView.as_view(), name="censo_create"),
    path('censo/<int:pk>/', CensoDetailView.as_view(), name='censo-detail'),
    path('censo/<int:pk>/export/', CensoExportView.as_view(), name='censo_export'),
    path('preguntacrearcenso/', CrearPreguntaViewCenso.as_view(), name='create_pregunta'),
    path('preguntacrearvotacion/', CrearPreguntaViewVotacion.as_view(), name='create_pregunta'),
    # path('preguntacrearrealizarvotacion/', CrearPreguntaViewRealizarVotacion.as_view(), name='create_pregunta'),
    path('realizarvotacion/', RealizarVotacion.as_view(), name='realizarvotacion'),
    path('', HomeView.as_view(), name="home"),
    path('ajax/load-preguntas/', load_preguntas, name='ajax_load_preguntas'),
    # path('votacionCompleja/', VotacionComplejaView.as_view(), name="votacioncompleja")
]


