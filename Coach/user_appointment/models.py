from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='', blank=False, null=False)
    last_name = models.CharField(max_length=30, default='', blank=False, null=False)
    email = models.EmailField(blank=False, default='')
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, default='')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentaires_rdv', null=True, blank=True)
