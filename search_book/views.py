import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from book.models import Book
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_books_by_ascending(request):
    books = Book.objects.all().order_by('title')
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

def get_books_by_descending(request):
    books = Book.objects.all().order_by('-title')
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")
    
def get_books_by_typing(request, typing):
    if len(typing) == 0:
        books = Book.objects.filter(title__contains=typing).order_by('?')
    
    else:
        books = Book.objects.filter(title__contains=typing).order_by('title')
    
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

@csrf_exempt
def filter_book_by_genre(request):
    if request.method == "POST":
        selected_genre = json.loads(request.body)

        if len(selected_genre) <= 0:
            books = Book.objects.all().order_by('?')

        else:
            books = Book.objects.filter(categories__in=selected_genre).order_by('title')

        return HttpResponse(serializers.serialize("json", books), content_type="application/json")


def search_book(request):
    books = Book.objects.all().order_by('?')
    context = {
        'books' : books
    }
    return render(request, 'search_books.html', context)

def navigation_to_review_book(request):
    return render(request, 'review_book.html', {})