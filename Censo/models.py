from django.db import models
from UsuarioUca.models import UsuarioUca
from django.urls import reverse_lazy


class Censo(models.Model):
    usuario = models.ManyToManyField(UsuarioUca,  blank=False, null=False)
    id_votacion = models.IntegerField()

    def get_absolute_url(self):
            return reverse_lazy('DetailCenso',  args=[str(self.id_votacion)])

        