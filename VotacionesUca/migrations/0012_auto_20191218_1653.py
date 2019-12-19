# Generated by Django 2.0 on 2019-12-18 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VotacionesUca', '0011_auto_20191218_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votacion',
            name='censo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Censo.Censo'),
        ),
        migrations.AlterField(
            model_name='votacion',
            name='pregunta',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='VotacionesUca.Pregunta'),
        ),
    ]