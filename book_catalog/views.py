from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from book.models import Book
from book_catalog.models import Review, WantToRead, Reading, Read
from user_registered.models import FavoriteBook
from book_catalog.forms import ReviewForm
from django.core import serializers
from django.contrib.auth.decorators import login_required

def book_show(request, id_buku):
    book = Book.objects.get(id=id_buku)
    reviewForm = ReviewForm(request.POST or None)
    reviews = Review.objects.filter(book=book)

    context = {
        'book': book,
        'reviewForm': reviewForm,
        'reviews': reviews,
    }
    return render(request, 'show.html', context)

# fungsi untuk menambahkan buku ke daftar buku yang ingin dibaca
@login_required(login_url='login')
@csrf_exempt
def add_want_to_read(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        want_to_read = WantToRead(book=add_book, user=add_user)
        want_to_read.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan buku ke daftar buku yang sedang dibaca
@login_required(login_url='login')
@csrf_exempt
def add_reading(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        reading = Reading(book=add_book, user=add_user)
        reading.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan buku ke daftar buku yang sudah dibaca
@login_required(login_url='login')
@csrf_exempt
def add_read(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        read = Read(book=add_book, user=add_user)
        read.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan komentar pada buku
@login_required(login_url='login')
@csrf_exempt
def add_review(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        add_review = request.POST['review']
        review = Review(book=add_book, user=add_user, review=add_review)
        review.save()
        return HttpResponseRedirect(reverse('book_catalog:show', args=(id_buku,)))
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk mengambil review dari buku
def get_reviews(request, id_buku):
    if request.method == "GET":
        book = Book.objects.get(pk=id_buku)
        review = Review.objects.filter(book=book)
        data = serializers.serialize('json', review)
        return HttpResponse(data, content_type='application/json')
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan ke favorite
@login_required(login_url='login')
@csrf_exempt
def add_favorite(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        favorite = FavoriteBook(book=add_book, user=add_user)
        favorite.save()
        return HttpResponseRedirect(reverse('book_catalog:show', args=(id_buku,)))
    return HttpResponseNotFound(b"NOT FOUND")