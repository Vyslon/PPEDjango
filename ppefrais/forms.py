from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'statut', 'adresse', 'code_postal', 'date_embauche')


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'statut', 'adresse', 'code_postal', 'date_embauche')
