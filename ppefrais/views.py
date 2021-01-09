from django.shortcuts import render
from django.http import Http404
from .models import FicheFrais, Visiteur, LigneFraisForfait, LigneFraisHorsForfait
from django.views.generic.edit import CreateView, UpdateView
import datetime


def fiches_frais(request):
    usr = Visiteur.objects.filter(id=request.user.id)[0]
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
    ficheFrais = FicheFrais.objects.filter(visiteur=usr).order_by('mois').extra(where=['mois>=%s'], params=[dateMinimum])
    nomMois = [moisEntier[int(elt.mois.strftime('%m').strip('0'))] for elt in ficheFrais]
    annee = [elt.mois.strftime('%Y') for elt in ficheFrais]

    context = {
        'fiches_nomMois': zip(ficheFrais, nomMois, annee)
    }

    return render(request, 'ficheFraisSelect.html', context)


def une_fiche_frais(request, mois):
    usr = request.user
    try:
        ficheFrais = FicheFrais.objects.get(mois=mois, visiteur=usr)
    except:
        raise Http404("Pas de fiche de frais correspondante")

    lignesFrais = LigneFraisForfait.objects.filter(fiche=ficheFrais)
    lignesFraisHF = LigneFraisHorsForfait.objects.filter(fiche=ficheFrais)

    context = {
        'ficheFrais': ficheFrais,
        'lignesFraisForfait': lignesFrais,
        'lignesFraisHorsForfait': lignesFraisHF
    }
    return render(request, 'ficheFrais.html', context)


class LigneFraisForfaitiseCreate(CreateView):
    model = LigneFraisForfait
    fields = ('frais_forfait', 'quantite')
    template_name = 'ligneFraisForfaitEdit.html'


class LigneFraisHorsForfaitCreate(CreateView):
    model = LigneFraisHorsForfait
    fields = '__all__'
    template_name = 'ligneFraisHorsForfaitEdit.html'


class LigneFraisForfaitUpdate(UpdateView):
    model = LigneFraisForfait
    fields = '__all__'
    template_name = 'ligneFraisForfaitEdit.html'


class LigneFraisForfaitHorsForfaitUpdate(UpdateView):
    model = LigneFraisHorsForfait
    fields = '__all__'
    template_name = 'ligneFraisHorsForfaitEdit.html'

