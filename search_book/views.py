import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from book.models import Book
from search_book.models import Request
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

@csrf_exempt
def add_request_book(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        year = request.POST.get("year")

        new_request = Request(title=title, author=author, year=year)
        new_request.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()