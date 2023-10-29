from django.db import models
from book.models import Book
from django.contrib.auth.models import User

class DiscussionThread(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    
class DiscussionReply(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)