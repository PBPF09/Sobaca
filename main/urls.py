from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from main.views import show_main, login_user, register, logout_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_registered/', include('user_registered.urls')),
    
]