# Generated by Django 2.2 on 2019-12-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsuarioUca', '0002_estudiante_pass_profesor'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariouca',
            name='rol',
            field=models.CharField(choices=[('Profesor', 'Profesor'), ('Estudiante', 'Estudiante'), ('PASS', 'PASSS')], default='Estudiante', max_length=10),
        ),
    ]
