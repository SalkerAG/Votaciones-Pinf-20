# Generated by Django 2.0 on 2019-12-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VotacionesUca', '0013_votacion_voto_restringido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votacion',
            name='voto_restringido',
        ),
        migrations.AddField(
            model_name='procesoelectoral',
            name='voto_restringido',
            field=models.BooleanField(default=False),
        ),
    ]