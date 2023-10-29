from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from book.models import Book

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE )
    name = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    fav_genre = models.CharField(max_length=150, null=True, blank=True)
    
    def __str__(self):
        return "{0}".format(self.user.email)
    
class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Quote(models.Model):
    text = models.TextField()