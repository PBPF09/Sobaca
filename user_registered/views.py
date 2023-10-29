from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

@login_required(login_url='/login')
def profile(request):
    if not Profile.objects.filter(user=request.user).exists():
        profile= Profile(user=request.user, name='', city='',fav_genre='')
        profile.save()
    else:
        profile =Profile.objects.get(user=request.user)

    context = {'username':request.user,
                'name': profile.name,
                'city': profile.city,
                'fav_genre': profile.fav_genre,
                }
    return render(request, 'profile.html', context)

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user.id)
        name = request.POST.get("name")
        city = request.POST.get("city")
        fav_genre = request.POST.get("fav_genre")
        user = request.user

        new_profile = Profile.objects.get(user= user)
        new_profile.name=name
        new_profile.city=city
        new_profile.fav_genre=fav_genre
        new_profile.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def get_profile(request):
    profile = Profile.objects.filter(user = request.user)
    return HttpResponse(serializers.serialize('json', profile))

@login_required(login_url='login')
@csrf_exempt
def favorite(request):       
    favorite_books = FavoriteBook.objects.filter(user=request.user)

    context = {
        'favorite_books': favorite_books,
    }
    return render(request, "favorite_books.html", context)

def get_favoriteBook(request):
    favorite_books = FavoriteBook.objects.filter(owner=request.user)
    return HttpResponse(serializers.serialize('json', favorite_books))

@csrf_exempt
def create_quote(request):
    if request.method == 'POST':
        text = request.POST.get("text")

        new_quote = Quote(text=text)
        new_quote.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def get_quote(request):
    quote = Quote.objects.all()
    return HttpResponse(serializers.serialize('json', quote))