from django.urls import path
from challenges.views import create_objective, edit_objective, complete_objective, objectives_list,get_objectives_json
from challenges.views import get_objectives_mobile, create_objective_mobile, delete_objective_mobile, edit_objective_mobile, complete_objective_mobile
app_name = 'challenges'

urlpatterns = [
    path('create_objective/', create_objective, name='create_objective'),
    path('edit_objective/<int:objective_id>/', edit_objective, name='edit_objective'),
    path('complete_objective/<int:objective_id>/', complete_objective, name='complete_objective'),
    path('objectives_list/', objectives_list, name='objectives_list'),
    path('get-objective/', get_objectives_json, name='get_product_json'),
    path('get_objectives_mobile/', get_objectives_mobile, name='get_product_mobile'),
    path('create_objective_mobile/', create_objective_mobile, name='create_objective_mobile'),
    path('delete_objective_mobile/', delete_objective_mobile, name='delete_objective_mobile'),
    path('edit_objective_mobile/', edit_objective_mobile, name='edit_objective_mobile'),
    path('complete_objective_mobile/', complete_objective_mobile, name='complete_objective_mobile'),
]