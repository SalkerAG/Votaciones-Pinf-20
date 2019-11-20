from django.db import models


class Censo(models.Model):
    id_usuario = models.CharField(max_length=8, blank=False, null=False, default=32085090, unique=True)
    id_votacion = models.IntegerField()