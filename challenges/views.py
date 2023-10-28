
from django.shortcuts import render, redirect
from challenges.models import Objective
from challenges.forms import ObjectiveForm 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

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
        objectives = Objective.objects.filter(is_completed=True)
    elif status == 'noncompleted':
        objectives = Objective.objects.filter(is_completed=False)
    else:
        objectives = Objective.objects.all()  


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

