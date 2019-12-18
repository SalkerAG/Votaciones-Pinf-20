# users/models.py
from django.apps import apps
from django.db import models
from UsuarioUca.models import UsuarioUca
#from VotacionesUca.models import ProcesoElectoral, Pregunta
from django.urls import reverse_lazy



class Censo(models.Model):
    usuario = models.ManyToManyField(UsuarioUca,  blank=False)
    #proceso = models.OneToOneField(ProcesoElectoral, on_delete=models.CASCADE)
    #pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT)

    def get_absolute_url(self):
            return reverse_lazy('DetailCenso',  args=[str(self.id_votacion)])

        