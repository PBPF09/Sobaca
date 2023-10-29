from django.shortcuts import render, redirect
from challenges.models import Objective
from challenges.forms import ObjectiveForm 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 


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
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        user = request.user

        new_product = Objective(name=name, price=price, description=description, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
def remove_product_ajax(request, id):
    Objective.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse("challenges:objective_list"))