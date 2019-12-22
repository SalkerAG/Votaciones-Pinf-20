# Generated by Django 2.0 on 2019-12-22 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Censo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_votacion', models.CharField(choices=[('0', 'Simple'), ('1', 'Compleja')], default='Simple', max_length=10)),
                ('enunciado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoElectoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto_restringido', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('es_consulta', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('procesoelectoral_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='VotacionesUca.ProcesoElectoral')),
                ('nie', models.IntegerField()),
                ('max_vacantes', models.IntegerField()),
                ('tipo_eleccion', models.BooleanField(default=False)),
            ],
            bases=('VotacionesUca.procesoelectoral',),
        ),
        migrations.CreateModel(
            name='UsuarioVotacion',
            fields=[
                ('Pregunta', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='VotacionesUca.Pregunta')),
                ('seleccion', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO'), ('ABSTENCIÓN', 'ABSTENCIÓN')], default='SI', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('procesoelectoral_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='VotacionesUca.ProcesoElectoral')),
                ('nombre_votacion', models.CharField(max_length=50, null=True)),
                ('es_presencial', models.BooleanField(default=False)),
                ('voto_rectificable', models.BooleanField(default=False)),
            ],
            bases=('VotacionesUca.procesoelectoral',),
        ),
        migrations.AddField(
            model_name='pregunta',
            name='opciones',
            field=models.ManyToManyField(to='VotacionesUca.Opcion'),
        ),
        migrations.AddField(
            model_name='censo',
            name='pregunta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Pregunta'),
        ),
        migrations.AddField(
            model_name='censo',
            name='usuario',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usuariovotacion',
            name='Votacion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Votacion'),
        ),
        migrations.AddField(
            model_name='usuariovotacion',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pregunta',
            name='Votacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='VotacionesUca.Votacion'),
        ),
        migrations.AddField(
            model_name='eleccion',
            name='censo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Censo'),
        ),
    ]