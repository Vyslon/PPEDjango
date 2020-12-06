import time

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import AuthenticationForm
from .models import Utilisateur


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ppefrais:home')

            context = {'form': form, 'errors': form.errors.items()}
            messages.error(request, "Le nom d'utilisateur ou le mot de passe est incorrect.")
            return render(request, 'ppefrais/connect.html', context)

    else:
        if request.user.is_authenticated:
            return redirect('ppefrais:home')

    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'ppefrais/connect.html', context)


def home(request):
    if request.user.is_authenticated:
        context = {
            'utilisateur': Utilisateur.objects.filter(user=request.user.id)[0]
        }
        return render(request, 'ppefrais/home.html', context)
    else:
        return redirect('ppefrais:index')


def disconnect(request):
    logout(request)
    return redirect('ppefrais:index')
