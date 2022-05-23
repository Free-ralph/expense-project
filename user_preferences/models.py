from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserPreference(models.Model):
    user = models.OneToOneField(User, related_name = "user_preference" ,on_delete = models.CASCADE)
    currency = models.CharField(max_length=4, default='USD')

    def __str__(self):
        return f"{self.user}'s preferences"