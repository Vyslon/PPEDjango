from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Visiteur(AbstractUser):
    adresse = models.CharField(max_length=30, null=True, blank=True)
    code_postal = models.CharField(max_length=5, null=True, blank=True)
    ville = models.CharField(max_length=30, null=True, blank=True)
    date_embauche = models.DateField(null=True, blank=True, default=timezone.now)

    class Meta:
        verbose_name = 'Visiteur médical'
        verbose_name_plural = 'Visiteurs médicaux'

    def __str__(self):
        return self.username


class FicheFrais(models.Model):
    class Etat(models.TextChoices):
        CLOTUREE = 'CL', _('Saisie clôturée')
        ENCOURS = 'CR', _('Fiche créée, saisie en cours')
        REMBOURSEE = 'RB', _('Remboursée')
        VALIDEE = 'VA', _('Validée et mise en paiement')

    etat = models.CharField(max_length=3, choices=Etat.choices, default=Etat.ENCOURS)
    visiteur = models.ForeignKey('Visiteur', on_delete=models.RESTRICT, default=None)
    mois = models.CharField(max_length=6, null=False)
    nb_justificatifs = models.PositiveIntegerField(null=True, blank=True, default=0)
    montant_valide = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)
    date_modif = models.DateField(null=True, default=timezone.datetime.now())

    class Meta:
        verbose_name = 'Fiche de frais'
        verbose_name_plural = 'Fiches de frais'
        unique_together = (('mois', 'visiteur'),)

    def get_absolute_url(self):
        return reverse('les-fiches')
    # TODO : corriger cette horreur / erreur

    def __str__(self):
        return self.mois + ' ' + self.visiteur.__str__()


class AbstractLigneFrais(models.Model):
    fiche = models.ForeignKey('FicheFrais', on_delete=models.RESTRICT, default=None)

    def __str__(self):
        return str(self.fiche.id) + str(self.id) + '(Abstr.)'

    class Meta:
        abstract = True


class LigneFraisHorsForfait(AbstractLigneFrais):
    libelle = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    montant = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return str(self.fiche.id) + str(self.id) + ' (H.F.)'

    class Meta:
        verbose_name = 'Ligne de frais (hors forfait)'
        verbose_name_plural = 'Lignes de frais (hors forfait)'


class LigneFraisForfait(AbstractLigneFrais):
    class FraisForfait(models.TextChoices):
        ETAPE = 'ETP', _('Forfait étape')
        FRAISKM = 'KM', _('Frais kilométrique')
        NUITHOTEL = 'NUI', _('Nuitée hôtel')
        RESTAU = 'REP', _('Repas restaurant')

    frais_forfait = models.CharField(max_length=3, choices=FraisForfait.choices, default=None)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return str(self.fiche.id) + str(self.id)

    class Meta:
        verbose_name = 'Ligne de frais'
        verbose_name_plural = 'Lignes de frais'
