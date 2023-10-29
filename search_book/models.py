from django.db import models

# Create your models here.
class Request(models.Model):
    title = models.TextField()
    author = models.TextField()
    year = models.IntegerField()