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
from .models import Profile
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
    product_item = Profile.objects.filter(user = request.user)
    return HttpResponse(serializers.serialize('json', product_item))

# @login_required(login_url='/login')
# def edit_profile(request):
#     if request.method == "POST":
#         profile = Profile.objects.get(user=request.user.id)
#         name = request.POST.get("name")
#         city = request.POST.get("city")
#         fav_genre = request.POST.get("fav_genre")

#         if name:
#             profile.name = name
#         if city:
#             profile.city = city
#         if fav_genre:
#             profile.fav_genre = fav_genre

#         profile.save()        
#         return redirect("profile")