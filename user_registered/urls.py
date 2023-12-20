from django.urls import include, path
from .views import *

app_name = 'user_registered'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('get_profile/', get_profile,name = 'get_profile'),
    path('favorite/', favorite, name='favorite'),
    path('delete_favorite/<int:book_id>/', delete_favorite, name='delete_favorite'),
    path("delete_favorite_ajax/<int:id>", delete_favorite_ajax, name="delete_favorite_ajax"),
    path("delete_favorite_flutter/<int:book_id>", delete_favorite_flutter, name="delete_favorite_flutter"),
    path('get_favorite/', get_favorite, name='get_favorite'),
    path('edit_profile_flutter/', edit_profile_flutter, name='edit_profile_flutter'),
]
