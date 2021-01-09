from django.urls import path
from . import views

urlpatterns = [
    path('fiches-frais/', views.fiches_frais, name='les-fiches'),
    path('fiches-frais/<str:mois>/saisie-frais-forfaitise/', views.LigneFraisForfaitiseCreate.as_view(), name='saisie-ligne-forfait'),
    path('fiches-frais/<str:mois>/saisie-frais-hors-forfait/', views.LigneFraisHorsForfaitCreate.as_view(), name='saisie-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/', views.une_fiche_frais, name='une-fiche'),
]
