from django.urls import path
from search_book.views import get_books_by_ascending, get_books_by_descending, get_books_by_typing, search_book, filter_book_by_genre, add_request_book, request_book, request_json, login

app_name = "search_book"

urlpatterns = [
    path('search/ascending/', get_books_by_ascending, name='get_books_by_ascending'),
    path('search/descending/', get_books_by_descending, name='get_books_by_descending'),
    path('<str:typing>', get_books_by_typing, name='get_books_by_typing'),
    path('filter/', filter_book_by_genre, name='filter_book_by_genre'),
    path('', search_book, name='search_book'),
    path('request-book/', add_request_book, name='add_request_book'),
    path('request/', request_book, name='request_book'),
    path('request-json/', request_json, name='request_json'),
    path('login/', login, name='login')
]