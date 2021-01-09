from django.urls import path
from . import views

urlpatterns = [
    path('fiches-frais/', views.fiches_frais, name='les-fiches'),
    path('fiches-frais/saisie-frais-forfaitise/', views.LigneFraisForfaitiseCreate.as_view, name='ligne-forfait'),
    path('fiches-frais/saisie-frais-hors-forfait/', views.LigneFraisHorsForfaitCreate.as_view, name='ligne-hors-forfait'),
    path('fiches-frais/<str:moisAnnee>/', views.une_fiche_frais, name='une-fiche'),
]
