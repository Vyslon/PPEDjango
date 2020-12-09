import time

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import FicheFrais


def fiches_frais(request):
    moisEntier = [
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

    ficheFrais = FicheFrais.objects.values('mois').distinct()
    nomMois = [moisEntier[int(elt['mois'])] for elt in ficheFrais]

    context = {
        'fiches_nomMois': zip(ficheFrais, nomMois),
        'size': len(nomMois)
    }

    return render(request, 'ficheFraisSelect.html', context)


def une_fiche_frais(request, mois):

    context = {
        'ficheFrais': FicheFrais.objects.filter(mois=mois, utilisateur_id=request.user.id)[0]
    }
    return render(request, 'ficheFrais.html', context)
