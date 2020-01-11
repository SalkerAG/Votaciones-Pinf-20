from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required

from UsuarioUca.views import HomeView, EstadisticasEleccionView
from . import views
from .views import CrearVotacionView, VotacionView, \
    CrearPregunta, CrearCensoVotacionView, CrearCensoEleccionView, CensoDetailView, CensoExportView, \
    CrearPreguntaVotacion, CrearPreguntaViewCenso, CrearPreguntaViewVotacion, \
    CrearPreguntaViewRealizarVotacion, load_preguntas, CrearPreguntaComplejaView, CrearEleccionView, ErrorVotacionView, \
    ExitoCensoVotacionView, EleccionView, CrearPersona, ListaVotacionesView, ListaEleccionesView, ListaCensosView, \
    VotacionUpdate, EleccionUpdate, CensoUpdate, EstadisticasVotacionSimpleView, EstadisticasVotacionComplejaView, \
    ErrorVotacionRectificableView

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacion"),
    path('eleccion/<slug:pk>', EleccionView.as_view(), name="eleccion"),
    path('crearpreguntacompleja/<slug:pk>', CrearPreguntaComplejaView.as_view(), name="crearpreguntacompleja"),
    path('crearpreguntavotacion/<slug:pk>', CrearPreguntaVotacion.as_view(), name="crearpreguntavotacion"),
    path('crearpregunta/', CrearPregunta.as_view(), name="crearpregunta"),
    path('crearcensoVotacion/', CrearCensoVotacionView.as_view(), name="censoV_create"),
    path('crearcensoEleccion/', CrearCensoEleccionView.as_view(), name="censoE_create"),
    path('censo/<int:pk>/', CensoDetailView.as_view(), name='censo-detail'),
    path('censo/<int:pk>/export/', CensoExportView.as_view(), name='censo_export'),
    path('preguntacrearcenso/', CrearPreguntaViewCenso.as_view(), name='create_pregunta'),
    path('preguntacrearvotacion/', CrearPreguntaViewVotacion.as_view(), name='create_pregunta'),
    path('creareleccion/', CrearEleccionView.as_view(), name='create_eleccion'),
    path('realizarvotacion/<int:pk>', VotacionView.as_view(), name='realizarvotacion'),
    path('', login_required(HomeView.as_view()), name="home"),
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
    path('eliminarpersona/<int:pk>', views.erase_persona, name="eliminar_persona"),
    path('eliminarrespuesta/<int:pk>', views.erase_respuesta, name="eliminar_respuesta"),
    path('estadisticasVotacionSimple/<int:pk>', EstadisticasVotacionSimpleView.as_view(), name="estadisticasvotacionsimple"),
    path('estadisticasVotacionCompleja/<int:pk>', EstadisticasVotacionComplejaView.as_view(), name="estadisticasvotacionsimple"),
    path('estadisticasEleccion/<int:pk>', EstadisticasEleccionView.as_view(), name="estadisticaseleccion"),
    path('errorVotacionRectificable/', ErrorVotacionRectificableView.as_view(), name="errorvotacionrectificable"),
    # path('creargrupo/', CrearPersonaGrupo.as_view(), name="crearpersonagrupo"),

]
