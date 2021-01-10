from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse

from .models import FicheFrais, Visiteur, LigneFraisForfait, LigneFraisHorsForfait
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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


class LigneFraisForfaitCreate(CreateView):
    model = LigneFraisForfait
    fields = ('frais_forfait', 'quantite')
    template_name = 'ligneFraisForfaitEdit.html'
    extra_context = {'edit': False}

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisForfaitCreate, self).form_valid(form)


class LigneFraisForfaitUpdate(UpdateView):
    model = LigneFraisForfait
    fields = ['quantite']
    template_name = 'ligneFraisForfaitEdit.html'
    extra_context = {'edit': True}

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisForfaitUpdate, self).form_valid(form)


class LigneFraisHorsForfaitCreate(CreateView):
    model = LigneFraisHorsForfait
    fields = ['libelle', 'date', 'montant']
    template_name = 'ligneFraisHorsForfaitEdit.html'

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisHorsForfaitCreate, self).form_valid(form)


class LigneFraisForfaitHorsForfaitUpdate(UpdateView):
    model = LigneFraisHorsForfait
    fields = ['libelle', 'date', 'montant']
    template_name = 'ligneFraisHorsForfaitEdit.html'

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisForfaitHorsForfaitUpdate, self).form_valid(form)


class LigneFraisHorsForfaitDelete(DeleteView):
    template_name = 'ligneFraisHorsForfaitConfirmDelete.html'
    model = LigneFraisHorsForfait

    def get_success_url(self):
        fiche = self.object.fiche
        return reverse('une-fiche', args=[(fiche.mois.strftime('%Y%m'))])
