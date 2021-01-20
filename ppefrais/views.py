from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse
from .models import FicheFrais, Visiteur, LigneFraisForfait, LigneFraisHorsForfait
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def une_fiche_frais_pdf(request, mois):
    template_path = 'ficheFraisPDF.html'

    usr = request.user
    try:
        ficheFrais = FicheFrais.objects.get(mois=mois, visiteur=usr)
    except:
        raise Http404("Pas de fiche de frais correspondante")

    if ficheFrais.etat == ficheFrais.Etat.ENCOURS:
        return redirect(reverse('une-fiche', args=[mois]))

    else:
        lignesFrais = LigneFraisForfait.objects.filter(fiche=ficheFrais)
        lignesFraisHF = LigneFraisHorsForfait.objects.filter(fiche=ficheFrais)

        context = {
            'ficheFrais': ficheFrais,
            'lignesFraisForfait': lignesFrais,
            'lignesFraisHorsForfait': lignesFraisHF
        }

        # Create a Django response object, and specify content_type as pdf
        if usr.first_name and usr.last_name:
            usrname = str(usr.id) + ' ' + usr.first_name + ' ' + usr.last_name
        else:
            usrname = str(usr.id) + ' ' + usr.username
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Fiche frais {mois}-VIS{usrname}.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


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
    usr = Visiteur.objects.filter(id=request.user.id)[0]

    dateMinimum = str(datetime.datetime.now().year - 1) + '01'
    ficheFrais = FicheFrais.objects.filter(visiteur=usr).order_by('mois').extra(where=['mois>=%s'],
                                                                                params=[dateMinimum])
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


class LigneFraisForfaitUpdate(UpdateView):
    model = LigneFraisForfait
    fields = ['quantite']
    template_name = 'ligneFraisForfaitEdit.html'

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisForfaitUpdate, self).form_valid(form)


class LigneFraisHorsForfaitCreate(CreateView):
    model = LigneFraisHorsForfait
    fields = ['libelle', 'date', 'montant']
    template_name = 'ligneFraisHorsForfaitEdit.html'
    extra_context = {'edit': False}

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisHorsForfaitCreate, self).form_valid(form)


class LigneFraisHorsForfaitUpdate(UpdateView):
    model = LigneFraisHorsForfait
    fields = ['libelle', 'date', 'montant']
    template_name = 'ligneFraisHorsForfaitEdit.html'
    extra_context = {'edit': True}

    def form_valid(self, form):
        fiche = get_object_or_404(FicheFrais, mois=self.kwargs['mois'])
        form.instance.fiche = fiche
        return super(LigneFraisHorsForfaitUpdate, self).form_valid(form)


class LigneFraisHorsForfaitDelete(DeleteView):
    template_name = 'ligneFraisHorsForfaitConfirmDelete.html'
    model = LigneFraisHorsForfait

    def get_success_url(self):
        fiche = self.object.fiche
        return reverse('une-fiche', args=[(fiche.mois.strftime('%Y%m'))])


class FicheFraisCreate(CreateView):
    model = FicheFrais
    template_name = 'nouvelleFicheFrais.html'
    fields = ('mois',)

    def form_valid(self, form):
        form.instance.visiteur = self.request.user
        return super(FicheFraisCreate, self).form_valid(form)
