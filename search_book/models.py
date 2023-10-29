from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField()
    author = models.TextField()
    year = models.IntegerField()