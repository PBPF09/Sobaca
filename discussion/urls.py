from django.urls import path
from discussion.views import *

app_name = 'discussion'

urlpatterns = [
    #Path yang digunakan untuk menampilkan halaman web
    path('', show_discussion, name='show_discussion'),
    path('start-discussion/', start_discussion, name='start_discussion'),
    path('threads/', join_discussion, name='join_discussion'),
    path('threads-view/<int:threadId>', detail_discussion, name='detail_discussion'),
    #Path yang digunakan untuk mengambil dan mengirimkan data
    path('get-book/', get_book_json, name='get_book_json'),
    path('get-threads/', get_thread_json, name='get_thread_json'),
    path('add-thread/', add_thread_discussion, name='add_thread_discussion'),
    path('get-reply/<int:threadId>', get_reply_thread, name='get_reply_thread'),
    path('add-reply/', add_reply_discussion, name='add_reply_discussion'),
]