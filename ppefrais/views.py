from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import FicheFrais, Etat, LigneFraisHorsForfait, CustomUser, LigneFraisForfait, FraisForfait
from django.views.generic.edit import CreateView
import datetime

def fiches_frais(request):
    usr = CustomUser.objects.filter(id=request.user.id)[0]
    moisEntier = [
        'None',
        'Janvier',
        'Février',
        'Mars',
        'Avril',
        'Mai',
        'Juin',
        'Juillet',
        'Août',
        'Septembre',
        'Octobre',
        'Novembre',
        'Décembre'
    ]

    dateMinimum = str(datetime.datetime.now().year - 1) + '01'
    ficheFrais = FicheFrais.objects.filter(utilisateur=usr).order_by('mois').extra(where=['mois>=%s'], params=[dateMinimum])
    nomMois = [moisEntier[int(elt.mois[4:6].strip('0'))] for elt in ficheFrais]
    annee = [elt.mois[0:4] for elt in ficheFrais]

    context = {
        'fiches_nomMois': zip(ficheFrais, nomMois, annee)
    }

    return render(request, 'ficheFraisSelect.html', context)


def une_fiche_frais(request, moisAnnee):
    usr = CustomUser.objects.filter(id=request.user.id)[0]
    try:
        ficheFrais = FicheFrais.objects.filter(mois=moisAnnee, utilisateur=usr)[0]
    except:
        raise Http404("Pas de fiche de frais correspondante")

    lignesFrais = LigneFraisForfait.objects.filter(utilisateur=usr, mois=moisAnnee)
    lignesFraisHF = LigneFraisHorsForfait.objects.filter(utilisateur=usr, mois=moisAnnee)


    context = {
        'ficheFrais': ficheFrais,
        'lignesFraisForfait': lignesFrais,
        'lignesFraisHorsForfait': lignesFraisHF
    }
    return render(request, 'ficheFrais.html', context)


class FicheCreate(CreateView):
    model = FicheFrais
    fields = '__all__'

