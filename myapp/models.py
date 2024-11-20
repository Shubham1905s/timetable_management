from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # You can add custom fields here if needed
    is_professor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    time_slot = models.TimeField()
    subject = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
