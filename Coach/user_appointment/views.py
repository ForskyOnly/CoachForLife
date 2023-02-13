from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from user_appointment.forms import CustomUserCreationForm

def home(request):
    return render(request, 'user_appointment/home.html')

class LoginView(LoginView):
    template_name = 'login.html'
    
class LogoutView(LogoutView):
    template_name = 'logout.html'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # définir des informations supplémentaires pour l'utilisateur ici
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required

def prendre_rdv(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        date = request.POST.get('date')
        # Création du rendez-vous
        appointment = Appointment.objects.create(
            user=request.user,
            date=date,
            
        )
        return redirect('calendar')
    return render(request, 'perndre_rdv.html')
