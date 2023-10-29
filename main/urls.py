<<<<<<< HEAD
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from main.views import show_main, login_user, register, logout_user
=======
from django.urls import path
from main.views import show_main, register, login_user, logout_user, guest, get_random_book
>>>>>>> e70c59f4128799aaf9ef56206d90ad9d9056f617

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
<<<<<<< HEAD
    path('user_registered/', include('user_registered.urls')),
    
=======
    path('guest/', guest, name='guest'),
    path('get_random_book/', get_random_book, name='get_random_book')
>>>>>>> e70c59f4128799aaf9ef56206d90ad9d9056f617
]