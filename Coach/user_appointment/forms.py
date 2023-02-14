from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom ")
    email = forms.EmailField()
    password1 = forms.CharField(label="Mot de passe *", widget=forms.PasswordInput, help_text="")
    password2 = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput, help_text="")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
