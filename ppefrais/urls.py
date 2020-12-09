from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('ficheFrais', views.fiches_frais),
    path('ficheFrais/<int:mois>/', views.une_fiche_frais)
]
