from django.urls import path
from . import views
from .views import FicheCreate

urlpatterns = [
    path('fiches-frais/', views.fiches_frais, name='les-fiches'),
    path('fiches-frais/<str:moisAnnee>/', views.une_fiche_frais, name='une-fiche'),
]
