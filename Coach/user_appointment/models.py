from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.forms.widgets import DateInput

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='', blank=False, null=False)
    last_name = models.CharField(max_length=30, default='', blank=False, null=False)
    email = models.EmailField(blank=False, default='')
    date = models.DateTimeField(default=timezone.now)
    widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
    duree = models.IntegerField(default=10)
    comment = models.TextField(null=False, blank=False, default='')
