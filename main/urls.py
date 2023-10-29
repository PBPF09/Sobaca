from django.urls import path
from main.views import show_main, register, login_user, logout_user, guest, get_random_book

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('guest/', guest, name='guest'),
    path('get_random_book/', get_random_book, name='get_random_book')
]