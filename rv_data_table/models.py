# models.py
from django.db import models
from django.contrib.auth.models import User

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"
