from django.db import models


class Etat(models.Model):
    libelle = models.CharField(max_length=30, null=True)


class Visiteur(models.Model):
    nom = models.CharField(max_length=30, null=True)
    prenom = models.CharField(max_length=30, null=True)
    adresse = models.CharField(max_length=30, null=True)
    code_postal = models.CharField(max_length=5, null=True)
    date_embauche = models.DateField(null=True)


class FicheFrais(models.Model):
    visiteur = models.ForeignKey('Visiteur', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    nb_justificatifs = models.PositiveIntegerField(null=True)
    montant_valide = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_modif = models.DateField(null=True)
    etat = models.ForeignKey('Etat', on_delete=models.RESTRICT, default=None)

    class Meta:
        unique_together = (('mois', 'visiteur'),)


class FraisForfait(models.Model):
    libelle = models.CharField(max_length=20, null=True)
    montant = models.DecimalField(max_digits=5, decimal_places=2, null=True)


class LigneFraisHorsForfait(models.Model):
    visiteur = models.ForeignKey('Visiteur', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    frais_forfait = models.ForeignKey('FraisForfait', on_delete=models.RESTRICT, default=None)
    quantite = models.PositiveIntegerField()
    bla

    class Meta:
        unique_together = (('visiteur','mois','frais_forfait'),)


