from django.contrib import admin

from book.models import Book
from book_catalog.models import WantToRead, Reading, Read, Review

# Register your models here.
admin.site.register(Book)
admin.site.register(WantToRead)
admin.site.register(Reading)
admin.site.register(Read)
admin.site.register(Review)