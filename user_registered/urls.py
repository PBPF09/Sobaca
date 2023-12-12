from django.urls import include, path
from .views import *

app_name = 'user_registered'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('get_profile/', get_profile,name = 'get_profile'),
    path('favorite/', favorite, name='favorite'),
    path('get_favorite/', get_favorite, name='get_favorite'),
    path('profile_flutter/', profile_flutter, name='profile_flutter'),
]
