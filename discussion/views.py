import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import DiscussionReply, DiscussionThread
from book.models import Book
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import ThreadForm, ReplyForm

# Create your views here.
@login_required(login_url='/login')
def show_discussion(request):
    context = {'user' : request.user}
    return render(request, "discussion_landing.html", context)

@login_required(login_url='/login')
def start_discussion(request):
    books = Book.objects.all()
    context = {'books' : books}
    return render(request, 'start_discussion.html', context)

@login_required(login_url='/login')
def join_discussion(request):
    threads = DiscussionThread.objects.all()
    context = {'threads' : threads}
    return render(request, 'discussion_center.html', context)

@login_required(login_url='/login')
def detail_discussion(request, threadId):
    thread = DiscussionThread.objects.get(pk=threadId)
    title = thread.title
    content = thread.content
    user = thread.user.username
    date_create = thread.date_create
    context = {'threadId' : threadId, 'title': title, 'content' : content, 'user' : user, 'date_create' : date_create }
    return render(request, 'discussion_detail.html', context)


def edit_thread(request, id):
    data = DiscussionThread.objects.get(pk = id)
    form = ThreadForm(request.POST or None, instance=data)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('discussion:join_discussion'))
    context = {'form': form}
    return render(request, "edit_thread.html", context)

def edit_reply(request, id):
    data = DiscussionReply.objects.get(pk = id)
    form = ReplyForm(request.POST or None, instance=data)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('discussion:join_discussion'))
    context = {'form': form}
    return render(request, "edit_reply.html", context)

def delete_reply(request, id):
    data = DiscussionReply.objects.filter(pk=id)
    data.delete()
    return redirect('discussion:detail_discussion' + id )

def get_book_json(request):
    book = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book))

@csrf_exempt
def add_thread_discussion(request):
    if request.method == 'POST':
        book = Book.objects.get(pk=request.POST.get("thread-bookId"))
        user = request.user
        title = request.POST.get("thread-title")
        content = request.POST.get("thread-content")
        
        new_thread = DiscussionThread(book=book, user=user, title=title, content=content)
        new_thread.save()
        return HttpResponse(b'CREATED', status=201)
    return HttpResponseNotFound()

def add_reply_discussion(request):
    if request.method == 'POST':
        thread = DiscussionThread.objects.get(pk=request.POST.get("reply-threadId"))
        user = request.user
        content = request.POST.get("reply-content")
        
        new_reply = DiscussionReply(thread=thread, user=user, content=content)
        new_reply.save()
        return HttpResponse(b'CREATED', status=201)
    return HttpResponseNotFound

def show_reply_json(request):
    data = DiscussionReply.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_thread_json(request):
    data = DiscussionThread.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    
def get_thread_json(request):
    threads = DiscussionThread.objects.all()
    thread_data = []
    
    for thread in threads:
        is_author = False
        if (request.user == thread.user):
            is_author = True
        thread_form = {
            'id' : thread.id,
            'user' : thread.user.username,
            'is_author' : is_author,
            'title' : thread.title,
            'content' : thread.content,
            'date_create' : thread.date_create,
            'book' : {
                'isbn' : thread.book.isbn,
                'title' : thread.book.title,
                'categories' : thread.book.categories,
                'author' : thread.book.author,
                'year' : thread.book.year,
                'publisher' : thread.book.publisher,
                'description' : thread.book.description,
                'image' : thread.book.images,   
            },
        }
        thread_data.append(thread_form)
    response = {'threads' : thread_data}
    return JsonResponse(response, safe=False)

def get_reply_thread(request, threadId):
    replys = DiscussionReply.objects.filter(thread=threadId)
    reply_data = []
    for reply in replys:
        is_author = False
        if (request.user == reply.user):
            is_author = True
        reply_form = {
            'id' : reply.id,
            'content' : reply.content,
            'user' : reply.user.username,
            'date_create' : reply.date_create,
            'is_author' : is_author,
            'thread' : {
                'title' : reply.thread.title,  
                'content' : reply.thread.content,  
                'user' : reply.thread.user.username,  
                'date_create' : reply.thread.date_create,
            }
        }
        reply_data.append(reply_form)
    response = {'replys' : reply_data}
    return JsonResponse(response, safe=False)

def get_thread_mobile(request):
    threads = DiscussionThread.objects.all()
    data = []
    user = request.user
    
    # if user.is_authenticated:
    user_id = user.id
    for thread in threads:
        is_author = False
        if (user_id == thread.user_id):
            is_author = True
        thread_form = {
            'id' : thread.id,
            'user' : thread.user.username,
            'is_author' : is_author,
            'title' : thread.title,
            'content' : thread.content,
            'date_create' : thread.date_create,
            'book' : {
                'isbn' : thread.book.isbn,
                'title' : thread.book.title,
                'author' : thread.book.author,
                'year' : thread.book.year,
                'publisher' : thread.book.publisher,
                'description' : thread.book.description,
                'image' : thread.book.images,   
            },
        }
        data.append(thread_form)
    # else:
    #     data = []
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type="application/json")

def get_reply_mobile(request, threadId):
    user = request.user
    replys = DiscussionReply.objects.filter(thread=threadId)
    data = []
    # if user.is_authenticated:
    user_id = user.id
    for reply in replys:
        is_author = False
        if (user_id == reply.user_id):
            is_author = True
        reply_form = {
            'id' : reply.id,
            'content' : reply.content,
            'user' : reply.user.username,
            'date_create' : reply.date_create,
            'is_author' : is_author,
            'thread' : {
                'title' : reply.thread.title,  
                'content' : reply.thread.content,  
                'user' : reply.thread.user.username,  
                'date_create' : reply.thread.date_create,
            }
        }
        data.append(reply_form)
    # else:
    #     data = []
    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def add_thread_mobile(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        newThread = DiscussionThread.objects.create(
            book = Book.objects.filter(id=int(data["bookId"])).get(),
            user = request.user,
            title = data["title"],
            content = data["content"]
        )

        newThread.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def add_reply_mobile(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        newReply = DiscussionReply.objects.create(
            thread = DiscussionThread.objects.filter(id=int(data["threadId"])).get(),
            user = request.user,
            content = data["content"]
        )

        newReply.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)