from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import FicheFrais, Etat, LigneFraisHorsForfait, CustomUser, LigneFraisForfait, FraisForfait
from django.views.generic.edit import CreateView

def fiches_frais(request):
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

    ficheFrais = FicheFrais.objects.values('mois').distinct()
    nomMois = [moisEntier[int(elt['mois'])] for elt in ficheFrais]

    context = {
        'fiches_nomMois': zip(ficheFrais, nomMois)
    }

    return render(request, 'ficheFraisSelect.html', context)


def une_fiche_frais(request, mois):
    usr = CustomUser.objects.filter(id=request.user.id)[0]
    try:
        ficheFrais = FicheFrais.objects.filter(mois=mois, utilisateur=usr)[0]
    except:
        raise Http404("Pas de fiche de frais correspondante")

    lignesFrais = LigneFraisForfait.objects.filter(utilisateur=usr, mois=mois)
    lignesFraisHF = LigneFraisHorsForfait.objects.filter(utilisateur=usr, mois=mois)


    context = {
        'etat': Etat.objects.filter(id=ficheFrais.etat.id)[0],
        'ficheFrais': ficheFrais,
        'lignesFraisForfait': lignesFrais,
        'lignesFraisHorsForfait': lignesFraisHF
    }
    return render(request, 'ficheFrais.html', context)


class FicheCreate(CreateView):
    model = FicheFrais
    fields = '__all__'
    template_name = 'ficheFraisCreate.html'
