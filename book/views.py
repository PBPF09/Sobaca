from django.http import HttpResponse
from django.core import serializers
from book.models import Book
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def get_books(request):
    data = Book.objects.all().order_by('?')
    return HttpResponse(serializers.serialize("json", data), content_type="application/json") 

# @login_required(login_url='/login')
def get_books_by_typing(request, typing):
    if len(typing) == 0:
        books = Book.objects.filter(
            Q(title__contains=typing) | Q(author__contains=typing)
            ).order_by('?')
    
    else:
        books = Book.objects.filter(
            Q(title__contains=typing) | Q(author__contains=typing)
            ).order_by('title')
    
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

# @login_required(login_url='/login')
def get_books_by_genre(request, genre):
    if genre == "All":
        books = Book.objects.all().order_by('?')
    
    else:
        books = Book.objects.filter(categories__contains=genre).order_by('title')
    
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

# @login_required(login_url='/login')
def order_books(request, order):
    if order == "ascending":
        # print(order)
        books = Book.objects.all().order_by('title')
    
    elif order == "descending":
        # print(order)
        books = Book.objects.all().order_by('-title')
    
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

