import json
from django.shortcuts import render, redirect
from challenges.models import Objective
from challenges.forms import ObjectiveForm 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.http import JsonResponse

def create_objective(request):
    if request.method == 'POST':
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)  
            objective.user = request.user  
            objective.save()  
            return HttpResponseRedirect(reverse('challenges:objectives_list'))  
    else:
        form = ObjectiveForm()
    
    return render(request, 'create_objective.html', {'form': form})

def objectives_list(request):
    status = request.GET.get('filter')
    if status == 'completed':
        objectives = Objective.objects.filter(user=request.user, is_completed=True)
    elif status == 'noncompleted':
        objectives = Objective.objects.filter(user=request.user, is_completed=False)
    else:
        objectives = Objective.objects.filter(user=request.user)  


    return render(request, 'objectives_list.html', {'objectives': objectives})


def edit_objective(request, objective_id):
    objective = Objective.objects.get(id=objective_id)
    form = ObjectiveForm(request.POST or None, instance=objective)
    
    if form.is_valid() and request.method == 'POST':
        form.save()
        return HttpResponseRedirect(reverse('challenges:objectives_list'))  
    
    return render(request, 'edit_objective.html', {'form': form})

def complete_objective(request, objective_id):
    objective = Objective.objects.get(id=objective_id)
    objective.is_completed = True
    objective.save()
    return HttpResponseRedirect(reverse('challenges:objectives_list'))



def get_objectives_json(request):
    objective_item = Objective.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', objective_item))


@csrf_exempt
def create_objective_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Objective(
            user = request.user,
            title = data["title"],
            description = data["description"],
        ).save()        
        return JsonResponse({"status": True}, status=200)
    
    return JsonResponse({"status": False}, status=400)

@csrf_exempt
def delete_objective_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        objective = Objective.objects.get(pk = data["id"])
        if objective.user == request.user:
            objective.delete()
            return JsonResponse({"status": True}, status=200)
    
    return JsonResponse({"status": False}, status=400)

@csrf_exempt
def edit_objective_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        objective = Objective.objects.get(pk = data["id"])
        if objective.user == request.user:
            objective.title = data["title"]
            objective.description = data["description"]
            objective.save()
            return JsonResponse({"status": True}, status=200)
    
    return JsonResponse({"status": False}, status=400)

@csrf_exempt
def complete_objective_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        objective = Objective.objects.get(pk = data["id"])
        if objective.user == request.user:
            objective.is_completed = True
            objective.save()
            return JsonResponse({"status": True}, status=200)
    
    return JsonResponse({"status": False}, status=400)

@csrf_exempt
def get_objectives_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data["status"])
        status = data["status"]
        if status == 'completed':
            objectives = Objective.objects.filter(user=request.user, is_completed=True)
        elif status == 'noncompleted':
            objectives = Objective.objects.filter(user=request.user, is_completed=False)
        else:
            objectives = Objective.objects.filter(user=request.user) 
        return HttpResponse(serializers.serialize('json', objectives), content_type="application/json")
    
    return HttpResponse(serializers.serialize('json', []), content_type="application/json")