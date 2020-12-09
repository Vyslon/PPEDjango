from django.urls import path
from .views import FicheCreate

urlpatterns = [
    path('ajouter-fiche/', FicheCreate.as_view(), name='ajouter-fiche'),
]
