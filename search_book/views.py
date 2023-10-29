import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from book.models import Book
from search_book.models import Request
from django.views.decorators.csrf import csrf_exempt
from search_book.forms import RequestForm
from django.db.models import Q

# Create your views here.
def get_books_by_ascending(request):
    books = Book.objects.all().order_by('title')
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

def get_books_by_descending(request):
    books = Book.objects.all().order_by('-title')
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")
    
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

@csrf_exempt
def add_request_book(request):
    form = RequestForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        book_request = form.save(commit=False)
        book_request.user = request.user
        book_request.save()
        return HttpResponseRedirect(reverse('search_book:search_book'))

    context = {
        'form': form
    }
    return render(request, "request_book.html", context)
