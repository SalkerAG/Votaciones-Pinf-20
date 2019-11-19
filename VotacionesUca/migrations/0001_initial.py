# Generated by Django 2.2 on 2019-11-19 17:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoElectoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('esConsulta', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('proceso', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='VotacionesUca.ProcesoElectoral')),
            ],
        ),
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('proceso', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='VotacionesUca.ProcesoElectoral')),
                ('esPresencial', models.BooleanField(default=False)),
                ('votoRectificable', models.BooleanField(default=False)),
                ('tipoVotacion', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('pregunta', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Pregunta')),
            ],
        ),
    ]
