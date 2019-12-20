from django.contrib import admin
from django.urls import path, include
from .views import CrearVotacionView, VotacionView, VotacionComplejaView, CrearPreguntaComplejaView, CrearPreguntaSimpleView

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacion"),
    path('crearpreguntacompleja/', CrearPreguntaComplejaView.as_view(), name="crearpreguntacompleja"),
    path('crearpreguntasimple/', CrearPreguntaSimpleView.as_view(), name="crearpreguntasimple"),
    # path('votacionCompleja/', VotacionComplejaView.as_view(), name="votacioncompleja")
]
