from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Book(models.Model):
    isbn = models.CharField(max_length=13, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    categories = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    images = models.CharField(max_length=100, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    name = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    fav_genre = models.CharField(max_length=150, null=True, blank=True)
    
    def __str__(self):
        return "{0}".format(self.user.email)