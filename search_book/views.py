import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from book.models import Book
from search_book.models import Request
from django.views.decorators.csrf import csrf_exempt
from search_book.forms import RequestForm
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
@login_required(login_url='/login')
def get_books_by_ascending(request):
    books = Book.objects.all().order_by('title')
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

@login_required(login_url='/login')
def get_books_by_descending(request):
    books = Book.objects.all().order_by('-title')
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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


@login_required(login_url='/login')
@csrf_exempt
def request_book(request):
    if request.method == 'POST':
        print(request.user)
        data = json.loads(request.body)

        new_request = Request.objects.create(
            user = request.user,
            title = data["title"],
            author = data["author"],
            year = data["year"],
        )

        new_request.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

# @login_required(login_url='/login')
def request_json(request):
    request_book = Request.objects.all()
    return HttpResponse(serializers.serialize("json", request_book), content_type="application/json")

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            print(request.user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
