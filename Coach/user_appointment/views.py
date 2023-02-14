from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from user_appointment.forms import CustomUserCreationForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test

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
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        date_str = request.POST.get('date')
        date = datetime.fromisoformat(date_str)
        hour = date.time().hour
        minute = date.time().minute
        weekday = date.weekday()
        # Vérification que le jour est compris entre lundi et vendredi
        if weekday < 0 or weekday > 4:
            return render(request, 'prendre_rdv.html', {'error_message': 'Vous pouvez prendre rendez-vous uniquement du lundi au vendredi'})
        # Vérification de la validité de l'heure
        if not ((9 <= hour < 12 and minute == 0) or (hour == 12 and minute == 30) or (13 <= hour < 17)):
            return render(request, 'prendre_rdv.html', {'error_message': 'Cette heure n\'est pas valide'})
        # Vérification de la disponibilité de l'heure
        time_with_hour_minute = date.replace(hour=hour, minute=minute)
        end_time = time_with_hour_minute + timedelta(minutes=10)
        if Appointment.objects.filter(date__range=[time_with_hour_minute, end_time]).exists():
            return render(request, 'prendre_rdv.html', {'error_message': 'Cette heure est déjà prise'})
        # Création du rendez-vous
        appointment = Appointment.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=time_with_hour_minute,
            duree=30
        )

        return redirect('home')
    # Affichage du formulaire de prise de rendez-vous
    return render(request, 'prendre_rdv.html')

@user_passes_test(lambda user: user.is_superuser)
def rdv_admin(request):
    appointments = Appointment.objects.all()
    return render(request, 'rdv_admin.html', {'appointments': appointments})

def mes_rdv(request):
    rdvs = Appointment.objects.filter(user=request.user)
    return render(request, 'mes_rdv.html', {'rdvs': rdvs})


def comment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        comment = request.POST.get('comment')
        appointment.comment = comment
        appointment.comment_author = request.user
        appointment.save()
        message = "Le commentaire a été ajouté avec succès."
    else:
        message = "Une erreur s'est produite lors de l'ajout du commentaire."
    
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments,
        'message': message,
    }
    return render(request, 'rdv_admin.html', context)