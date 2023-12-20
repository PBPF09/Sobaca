import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from book.models import Book
from book_catalog.models import Review, WantToRead, Reading, Read
from book_catalog.forms import ReviewForm
from django.core import serializers
from django.contrib.auth.decorators import login_required

from user_registered.models import Profile

def book_show(request, id_buku):
    book = Book.objects.get(id=id_buku)
    reviewForm = ReviewForm(request.POST or None)
    reviews = Review.objects.filter(book=book)

    context = {
        'book': book,
        'id_buku': book.id,  
        'id_user': request.user.id,  
        'reviewForm': reviewForm,
        'reviews': reviews,
    }
    return render(request, 'show.html', context)

# fungsi untuk menambahkan buku ke daftar buku yang ingin dibaca
@login_required(login_url='login')
@csrf_exempt
def add_want_to_read(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        want_to_read = WantToRead(book=add_book, user=add_user)
        want_to_read.save()
        return JsonResponse({'status' : 'success'})
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan buku ke daftar buku yang sedang dibaca
@login_required(login_url='login')
@csrf_exempt
def add_reading(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        reading = Reading(book=add_book, user=add_user)
        reading.save()
        return JsonResponse({'status' : 'success'})
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan buku ke daftar buku yang sudah dibaca
@login_required(login_url='login')
@csrf_exempt
def add_read(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        read = Read(book=add_book, user=add_user)
        read.save()
        return JsonResponse({'status' : 'success'})
    return HttpResponseNotFound(b"NOT FOUND")

# fungsi untuk menambahkan komentar pada buku
@login_required(login_url='login')
@csrf_exempt
def add_review(request, id_buku):
    if request.method == "POST":
        add_book = Book.objects.get(pk=id_buku)
        add_user = request.user
        add_review = request.POST['review']
        review = Review(book=add_book, user=add_user, review=add_review)
        review.save()
        return HttpResponse(b'CREATED', status=201)
    return HttpResponseNotFound(b"NOT FOUND")

def get_reviews(request, id_buku):
    book = Book.objects.get(pk=id_buku)
    reviews = Review.objects.filter(book=book)

    # Bangun list manual berisi informasi yang diinginkan
    review_data = []
    for review in reviews:
        review_form = {
            'review_id': review.id,
            'user_id': review.user.id,
            'username': review.user.username,
            'book': review.book.id,
            'review': review.review,
            'waktu': review.waktu,
        }
        review_data.append(review_form)

    # Menggunakan JsonResponse untuk mengirimkan data JSON
    response = {'reviews' : review_data}
    return JsonResponse(review_data, safe=False)
    
def show_review_json(request, id_buku):
    data = Review.objects.filter(book=id_buku)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

# fungsi untuk menambahkan ke favorite
@login_required(login_url='login')
@csrf_exempt
def add_favorite(request, id_buku, id_user):
    book = Book.objects.get(pk=id_buku)
    user_profile = Profile.objects.get(user=request.user)
    user_profile.favorite_books.add(book)
    return HttpResponseRedirect(reverse('book_catalog:show', args=(id_buku,)))

@csrf_exempt
def add_favorite_flutter(request, book_id):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        favorite_books = user_profile.favorite_books.all()
        add_book = Book.objects.get(id=book_id)

        user_profile.favorite_books.add(add_book)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def add_review_flutter(request, book_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            # Ensure the user is authenticated before allowing them to submit a review
            if not request.user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

            newReview = Review.objects.create(
                user=request.user,
                book=Book.objects.get(id=book_id),
                review=data['review']
            )

            newReview.save()
            return JsonResponse({"status": "success"}, status=201)
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def get_review(request, review_id):
    review = Review.objects.get(id=review_id)
    return JsonResponse({"review": review.review}, status=200)

@login_required(login_url='login')
@csrf_exempt
def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == "POST":
        data = json.loads(request.body)
        review.review = data['review']
        review.save()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_review(request, review_id):
    if request.method == "DELETE":
        review = Review.objects.get(id=review_id)
        review.delete()
        return HttpResponse(b"OK", status=200)
    return HttpResponseNotFound(b"NOT FOUND")
        
# cek apakah id buku ada di daftar favorit user
@login_required(login_url='login')
@csrf_exempt
def is_favorite(request, id_buku):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        favorite_books = user_profile.favorite_books.all()
        book = Book.objects.get(pk=id_buku)
        if book in favorite_books:
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "error"}, status=401)

def get_user_book_data(request):
    try:
        user_want_to_read = WantToRead.objects.filter(user=request.user)
        user_reading = Reading.objects.filter(user=request.user)
        user_read = Read.objects.filter(user=request.user)

        want_to_read_data = [{
            'isbn': item.book.isbn,
            'title': item.book.title, 
            'categories': item.book.categories,
            'author': item.book.author, 
            'year': item.book.year,
            'publisher': item.book.publisher,
            'description': item.book.description,
            'images': item.book.images} for item in user_want_to_read]
        reading_data = [{
            'isbn': item.book.isbn,
            'title': item.book.title, 
            'categories': item.book.categories,
            'author': item.book.author, 
            'year': item.book.year,
            'publisher': item.book.publisher,
            'description': item.book.description,
            'images': item.book.images} for item in user_reading]
        read_data = [{
            'isbn': item.book.isbn,
            'title': item.book.title, 
            'categories': item.book.categories,
            'author': item.book.author, 
            'year': item.book.year,
            'publisher': item.book.publisher,
            'description': item.book.description,
            'images': item.book.images} for item in user_read]

        return JsonResponse({
            'want_to_read': want_to_read_data,
            'reading': reading_data,
            'read': read_data,
            'status' : 'success',
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})
