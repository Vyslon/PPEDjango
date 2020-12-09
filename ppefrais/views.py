from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import FicheFrais
from django.views.generic.edit import CreateView


class FicheCreate(CreateView):
    model = FicheFrais
    fields = '__all__'
