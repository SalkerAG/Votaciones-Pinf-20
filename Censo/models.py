from django.db import models


class UsuarioUcausuariouca(models.Model): # Clase para tomar los valores de la tabla UsuarioUca_usuariouca
    first_name = models.CharField(max_length=30) # first_name registro de la tabla UsuarioUca_usuariouca
    last_name = models.CharField(max_length=150) # last_name registro de la tabla UsuarioUca_usuariouca

    class Meta: # esta clase nos permite poder definir la base datos asociada, nombre de la tabla
        managed = False # falso = no crea tabla, true = crearia una tabla con los registros de arriba.
        db_table = 'UsuarioUca_usuariouca' # Nombre de la tabla asociada al modelo.

#def __str__(self):
    #return self.first_name

class Post(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)