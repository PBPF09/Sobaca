from django.urls import path
from book_catalog.views import book_show, add_want_to_read, add_reading, add_read, add_review, get_reviews, add_favorite

app_name = 'book_catalog'

urlpatterns = [
    path('show/<int:id_buku>/', book_show, name='show'),
    path('add-want-to-read/<int:id_buku>', add_want_to_read, name='add_want_to_read'),
    path('add-reading/<int:id_buku>', add_reading, name='add_reading'),
    path('add-read/<int:id_buku>', add_read, name='add_read'),
    path('add-review/<int:id_buku>', add_review, name='add_review'),
    path('get-reviews/<int:id_buku>', get_reviews, name='get_reviews'),
    path('add-favorite/<int:id_buku>/<int:id_user>/', add_favorite, name='add_favorite'),
]