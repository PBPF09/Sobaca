from django.urls import path
from authentication.views import login, register_flutter, logout

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register_flutter/', register_flutter, name='register_flutter'),
    path('logout/', logout, name='logout'),
]