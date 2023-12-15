import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse, JsonResponse
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

    context = {'user': request.user,
               'username': request.user.username,
                'name': profile.name,
                'city': profile.city,
                'fav_genre': profile.fav_genre,
                }
    return render(request, 'profile.html', context)

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user.id)
        username = request.POST.get('username')
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
    user_profile = Profile.objects.get(user=request.user)
    favorite_books = user_profile.favorite_books.all()
    context = {'favorite_books': favorite_books}
    return render(request, "favorite_books.html", context)

def get_favorite(request):
    user_profile = Profile.objects.get(user=request.user)
    favorite_books = user_profile.favorite_books.all()
    return HttpResponse(serializers.serialize('json', favorite_books))

@csrf_exempt   
def edit_profile_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        new_profile = Profile.objects.get(user=request.user)

        # Update the profile fields
        new_profile.name = data['name']
        new_profile.city = data['city']
        new_profile.fav_genre = data['fav_genre']

        # Save the changes
        new_profile.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)