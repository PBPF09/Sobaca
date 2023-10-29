from django.urls import include, path
from .views import *

app_name = 'user_registered'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('get_profile', get_profile,name = 'get_profile')
]
