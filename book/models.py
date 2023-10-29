from django.db import models

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    categories = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    images = models.CharField(max_length=100, null=True, blank=True)