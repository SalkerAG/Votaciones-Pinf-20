from django.contrib import admin
from django.urls import path, include

from UsuarioUca.views import HomeView
from . import views
from .views import CrearVotacionView, VotacionView, \
    CrearPregunta, CrearCensoView, CensoDetailView, CensoExportView, \
    CrearPreguntaVotacion, CrearPreguntaViewCenso, CrearPreguntaViewVotacion, \
    CrearPreguntaViewRealizarVotacion, load_preguntas, CrearPreguntaComplejaView, CrearEleccionView, ErrorVotacionView, \
    ExitoCensoVotacionView, EleccionView, CrearPersona, ListaVotacionesView, ListaEleccionesView, ListaCensosView, \
    VotacionUpdate,EleccionUpdate,CensoUpdate

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacion"),
    path('eleccion/<slug:pk>', EleccionView.as_view(), name="eleccion"),
    path('crearpreguntacompleja/<slug:pk>', CrearPreguntaComplejaView.as_view(), name="crearpreguntacompleja"),
    # path('crearpreguntasimple/', CrearPreguntaSimpleView.as_view(), name="crearpreguntasimple"),
    path('crearpreguntavotacion/<slug:pk>', CrearPreguntaVotacion.as_view(), name="crearpreguntavotacion"),
    path('crearpregunta/', CrearPregunta.as_view(), name="crearpregunta"),
    path('crearcenso/', CrearCensoView.as_view(), name="censo_create"),
    path('censo/<int:pk>/', CensoDetailView.as_view(), name='censo-detail'),
    path('censo/<int:pk>/export/', CensoExportView.as_view(), name='censo_export'),
    path('preguntacrearcenso/', CrearPreguntaViewCenso.as_view(), name='create_pregunta'),
    path('preguntacrearvotacion/', CrearPreguntaViewVotacion.as_view(), name='create_pregunta'),
    path('creareleccion/', CrearEleccionView.as_view(), name='create_eleccion'),
    # path('preguntacrearrealizarvotacion/', CrearPreguntaViewRealizarVotacion.as_view(), name='create_pregunta'),
    path('realizarvotacion/<int:pk>', VotacionView.as_view(), name='realizarvotacion'),
    path('', HomeView.as_view(), name="home"),
    path('ajax/load-preguntas/', load_preguntas, name='ajax_load_preguntas'),
    path('creareleccion/', CrearEleccionView.as_view(), name='create_eleccion'),
    path('errorVotacion/', ErrorVotacionView.as_view(), name='errorvotacion'),
    path('exitocensovotacion/', ExitoCensoVotacionView.as_view(), name='exitocensovotacion'),
    path('crearpersona/<slug:pk>', CrearPersona.as_view(), name="crearpersona"),
    path('listavotaciones/', ListaVotacionesView.as_view(), name="listavotaciones"),
    path('editarvotacion/<int:pk>', VotacionUpdate.as_view(), name='votacion_edit'),
    path('eliminarvotacion/<int:pk>', views.erase_request1, name="eliminar_votacion"),
    path('listaelecciones/', ListaEleccionesView.as_view(), name="listaelecciones"),
    path('editareleccion/<int:pk>', EleccionUpdate.as_view(), name='eleccion_edit'),
    path('eliminareleccion/<int:pk>', views.erase_request2, name="eliminar_eleccion"),
    path('listacensos/', ListaCensosView.as_view(), name="listacensos"),
    path('editarcenso/<int:pk>', CensoUpdate.as_view(), name='censo_edit'),
    path('eliminarcenso/<int:pk>', views.erase_request3, name="eliminar_censo"),
    # path('creargrupo/', CrearPersonaGrupo.as_view(), name="crearpersonagrupo"),

    # path('creartipoeleccion/', CrearTipoEleccionView.as_view(), name="creartipoeleccion"),

    # path('votacionCompleja/', VotacionComplejaView.as_view(), name="votacioncompleja")
]
