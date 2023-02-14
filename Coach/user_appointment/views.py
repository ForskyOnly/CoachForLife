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
    """
    Permet aux utilisateurs de s'inscrire et crée un nouvel utilisateur.
    """
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
    """
    Permet aux utilisateurs connectés de prendre un rendez-vous en utilisant un formulaire. si l'horraire est valide 
    et disponile un rendez-vous est crée
    """
    if request.method == 'POST':
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        date_str = request.POST.get('date')
        date = datetime.fromisoformat(date_str)
        hour = date.time().hour
        minute = date.time().minute
        weekday = date.weekday()
        if weekday < 0 or weekday > 4:
            return render(request, 'prendre_rdv.html', {'error_message': 'Vous pouvez prendre rendez-vous uniquement du lundi au vendredi'})
        if not ((9 <= hour < 12 and minute == 0) or (hour == 12 and minute == 30) or (13 <= hour < 17)):
            return render(request, 'prendre_rdv.html', {'error_message': 'Cette heure n\'est pas valide'})
        time_with_hour_minute = date.replace(hour=hour, minute=minute)
        end_time = time_with_hour_minute + timedelta(minutes=10)
        if Appointment.objects.filter(date__range=[time_with_hour_minute, end_time]).exists():
            return render(request, 'prendre_rdv.html', {'error_message': 'Cette heure est déjà prise'})
        appointment = Appointment.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=time_with_hour_minute,
            duree=30
        )

        return redirect('mes_rdv')
    return render(request, 'prendre_rdv.html')

@user_passes_test(lambda user: user.is_superuser)
def rdv_admin(request):
    """
    Permet à l'administrateur de voir tous les rendez-vous et de commenter un rendez-vous spécifique.
    """
    appointments = Appointment.objects.all()
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        comment = request.POST.get('comment')
        appointment.comment = comment
        appointment.comment_author = request.user
        appointment.save()
        return redirect('rdv_admin')
    return render(request, 'rdv_admin.html', {'appointments': appointments})

def mes_rdv(request):
    """
    Affiche les rendez-vous des utilisateurs connectés.
    """
    rdvs = Appointment.objects.filter(user=request.user)
    return render(request, 'mes_rdv.html', {'rdvs': rdvs})


@user_passes_test(lambda user: user.is_superuser)
def comment(request, appointment_id):
    """
    Permet à l'administrateur d'ajouter un commentaire à un rendez-vous spécifique.
    """
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        comment = request.POST.get('comment')
        appointment.comment = comment
        appointment.comment_author = request.user
        appointment.save()
        message = "Le commentaire a été ajouté avec succès."
        return redirect('rdv_admin')
    else:
        message = "Une erreur s'est produite lors de l'ajout du commentaire."
    
    rdvs = Appointment.objects.filter(user=request.user)
    context = {
        'rdvs': rdvs,
        'message': message,
    }
    return render(request, 'rdv_admin.html', context)
