from django import forms


class AuthenticationForm(forms.Form):
    """
    Forms for authentication, used by "connect" view
    """
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(label="Mot de passe", max_length=50, widget=forms.PasswordInput)
