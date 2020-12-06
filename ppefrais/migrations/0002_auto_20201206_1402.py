# Generated by Django 3.1.4 on 2020-12-06 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppefrais', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichefrais',
            name='utilisateur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lignefraishorsforfait',
            name='utilisateur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fichefrais',
            unique_together={('mois', 'utilisateur')},
        ),
        migrations.AlterUniqueTogether(
            name='lignefraishorsforfait',
            unique_together={('utilisateur', 'mois', 'frais_forfait')},
        ),
    ]
