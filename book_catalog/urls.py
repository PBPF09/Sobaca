from django.urls import path
from book_catalog.views import book_show, book_add, book_edit, book_delete

app_name = 'book_catalog'

urlpatterns = [
    path('show/<int:id_buku>/', book_show, name='show'),
    path('add/', book_add, name='add'),
    path('edit/<int:id_buku>/', book_edit, name='edit'),
    path('delete/<int:id_buku>/', book_delete, name='delete'),
]