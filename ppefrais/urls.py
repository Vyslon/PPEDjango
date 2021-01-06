from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from .views import FicheCreate

urlpatterns = [
    path('ficheFrais', views.fiches_frais, name='les-fiches'),
    path('ficheFrais/<str:moisAnnee>/', views.une_fiche_frais, name='une-fiche'),
    path('ajouter-fiche/', FicheCreate.as_view(), name='ajouter-fiche')
]