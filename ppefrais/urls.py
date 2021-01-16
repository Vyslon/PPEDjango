from django.urls import path
from . import views

urlpatterns = [
    path('fiches-frais/', views.fiches_frais, name='les-fiches'),
    path('fiches-frais/nouvelle-fiche/', views.FicheFraisCreate.as_view(), name='nouvelle-fiche-frais'),
    path('fiches-frais/<str:mois>/saisie-frais-hors-forfait/', views.LigneFraisHorsForfaitCreate.as_view(), name='saisie-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/edition-frais-forfaitaire/<int:pk>/', views.LigneFraisForfaitUpdate.as_view(), name='edit-ligne-forfait'),
    path('fiches-frais/<str:mois>/edition-frais-hors-forfait/<int:pk>/', views.LigneFraisHorsForfaitUpdate.as_view(), name='edit-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/suppression-frais-hors-forfait/<int:pk>/', views.LigneFraisHorsForfaitDelete.as_view(), name='suppr-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/pdf/', views.une_fiche_frais_pdf, name='une-fiche-pdf'),
    path('fiches-frais/<str:mois>/', views.une_fiche_frais, name='une-fiche'),
]
