from django.urls import path
from book.views import get_books, get_books_by_typing, get_books_by_genre, get_books_by_typing, order_books

app_name = "book"

urlpatterns = [
    path("", get_books, name="get_books"),
    path("<str:typing>", get_books_by_typing, name="get_books_by_typing"),
    path("genres/<str:genre>", get_books_by_genre, name="get_books_by_genre"),
    path("order-by/<str:order>/", order_books, name="order_books")
]