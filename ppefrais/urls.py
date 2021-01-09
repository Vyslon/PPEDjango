from django.urls import path
from . import views
from .views import FicheCreate

urlpatterns = [
    path('ficheFrais', views.fiches_frais, name='les-fiches'),
    path('ficheFrais/<str:moisAnnee>/', views.une_fiche_frais, name='une-fiche'),
    path('saisir-frais/', views.saisir_frais, name='saisir-frais'),
]
