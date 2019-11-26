# Generated by Django 2.2.7 on 2019-11-26 18:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Censo', '0003_remove_censo_id_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='censo',
            name='usuario',
        ),
        migrations.AddField(
            model_name='censo',
            name='usuario',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
