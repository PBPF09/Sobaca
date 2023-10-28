from django.urls import path
from challenges.views import create_objective, edit_objective, complete_objective, objectives_list,get_objectives_json,add_product_ajax,remove_product_ajax

app_name = 'challenges'

urlpatterns = [
    path('create_objective/', create_objective, name='create_objective'),
    path('edit_objective/<int:objective_id>/', edit_objective, name='edit_objective'),
    path('complete_objective/<int:objective_id>/', complete_objective, name='complete_objective'),
    path('objectives_list/', objectives_list, name='objectives_list'),
    path('get-objective/', get_objectives_json, name='get_product_json'),

]