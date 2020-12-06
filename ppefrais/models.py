from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Etat(models.Model):
    libelle = models.CharField(max_length=30, null=True)


class FicheFrais(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    nb_justificatifs = models.PositiveIntegerField(null=True)
    montant_valide = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_modif = models.DateField(null=True)
    etat = models.ForeignKey('Etat', on_delete=models.RESTRICT, default=None)

    class Meta:
        unique_together = (('mois', 'utilisateur'),)


class FraisForfait(models.Model):
    libelle = models.CharField(max_length=20, null=True)
    montant = models.DecimalField(max_digits=5, decimal_places=2, null=True)


class LigneFraisHorsForfait(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    frais_forfait = models.ForeignKey('FraisForfait', on_delete=models.RESTRICT, default=None)
    quantite = models.PositiveIntegerField()

    class Meta:
        unique_together = (('utilisateur', 'mois', 'frais_forfait'),)


class Utilisateur(models.Model):
    class Statut(models.TextChoices):
        VST = "Visiteur"
        CPT = "Comptable"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    statut = models.CharField(
        max_length=9,
        choices=Statut.choices,
        default=Statut.CPT
    )
    adresse = models.CharField(max_length=30, null=True)
    code_postal = models.CharField(max_length=5, null=True)
    date_embauche = models.DateField(null=True)

