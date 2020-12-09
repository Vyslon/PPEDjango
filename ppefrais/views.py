import time

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

def ficheFrais(request):
    context = {}
    return render(request, 'ficheFrais.html')

