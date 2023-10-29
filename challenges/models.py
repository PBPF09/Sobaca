from django.db import models
from django.contrib.auth.models import User

class Objective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


