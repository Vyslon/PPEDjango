from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class AuthenticationForm(forms.Form):
    """
    Forms for authentication, used by "connect" view
    """
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(label="Mot de passe", max_length=50, widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
