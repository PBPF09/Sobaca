from django.urls import path
from book_catalog.views import *
app_name = 'book_catalog'

urlpatterns = [
    path('show/<int:id_buku>/', book_show, name='show'),
    path('add-want-to-read/<int:id_buku>', add_want_to_read, name='add_want_to_read'),
    path('add-reading/<int:id_buku>', add_reading, name='add_reading'),
    path('add-read/<int:id_buku>', add_read, name='add_read'),
    path('add-review/<int:id_buku>', add_review, name='add_review'),
    path('get-reviews/<int:id_buku>', get_reviews, name='get_reviews'),
    path('add-favorite/<int:id_buku>/<int:id_user>/', add_favorite, name='add_favorite'),
    path('show-review-json/<int:id_buku>', show_review_json, name='show_review_json'),
    path('add-favorite-flutter/<int:book_id>/', add_favorite_flutter, name='add_favorite_flutter'),
    path('add-review-flutter/<int:book_id>/', add_review_flutter, name='add_review_flutter'),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),
    path('get-review/<int:review_id>/', get_review, name='get_review'),
    path('is-favorite/<int:id_buku>/', is_favorite, name='is_favorite'),
    path('get-user-book-data/', get_user_book_data, name='get_user_book_data'),
]