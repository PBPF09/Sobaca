import datetime
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from book.models import Book
from django.http import JsonResponse

@login_required(login_url='/login')
def show_main(request):

    if 'last_login' in request.COOKIES:
        last_login = request.COOKIES['last_login']
    else:
        last_login = 'N/A'
    context = {
        'name': 'Sobaca',
 
        'last_login' : last_login
    }
    return render(request, "main.html", context)


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)



def login_user(request):
    random_id = random.randint(1,Book.objects.count())
    books = Book.objects.get(pk=random_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {'random_book' : books}
    return render(request, 'login.html', context)



def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def guest(request):
    return render(request, 'main.html')

from django.http import JsonResponse

def get_random_book(request):
    random_id = random.randint(1, Book.objects.count())
    random_book = Book.objects.get(pk=random_id)
    data = {
        'title': random_book.title,
        'author': random_book.author,
        'image_url': random_book.images
    }
    return JsonResponse(data)
