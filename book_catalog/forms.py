from django.forms import ModelForm
from book.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'categories', 'author', 'year', 'publisher', 'description', 'images']