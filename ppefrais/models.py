from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    class Statut(models.TextChoices):
        VISITEUR = 'VST', _('Visiteur')
        COMPTABLE = 'CPT', _('Comptable')

    statut = models.CharField(max_length=3, choices=Statut.choices, default=Statut.COMPTABLE)
    adresse = models.CharField(max_length=30, null=True, blank=True)
    code_postal = models.CharField(max_length=5, null=True, blank=True)
    date_embauche = models.DateField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.username


class Etat(models.Model):
    libelle = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.libelle


class FicheFrais(models.Model):
    utilisateur = models.ForeignKey('CustomUser', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    nb_justificatifs = models.PositiveIntegerField(null=True)
    montant_valide = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_modif = models.DateField(null=True)
    etat = models.ForeignKey('Etat', on_delete=models.RESTRICT, default=None)

    class Meta:
        unique_together = (('mois', 'utilisateur'),)

    def __str__(self):
        return self.mois + ' ' + self.utilisateur.__str__()


class FraisForfait(models.Model):
    libelle = models.CharField(max_length=20, null=True)
    montant = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.libelle


class AbstractLigneFraisForfait(models.Model):
    utilisateur = models.ForeignKey('CustomUser', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    frais_forfait = models.ForeignKey('FraisForfait', on_delete=models.RESTRICT, default=None)
    quantite = models.PositiveIntegerField()
    date = models.DateField(null=True)

    class Meta:
        unique_together = (('utilisateur', 'mois', 'frais_forfait'),)
        abstract = True

    def __str__(self):
        return self.date.__str__() + ' ' + self.utilisateur.__str__()


class LigneFraisHorsForfait(AbstractLigneFraisForfait):
    pass


class LigneFraisForfait(AbstractLigneFraisForfait):
    pass
