from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from book.models import Book
from book_catalog.forms import BookForm

def book_show(request, id_buku):
    book = Book.objects.get(id=id_buku)
    context = {'book': book}
    return render(request, 'show.html', context)

def book_add(request):
    if Book.objects.count() >= 101:
        return HttpResponseRedirect(reverse('book_catalog:show', args=(1,)))
    form = BookForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        book = form.save(commit=False)
        book.user = request.user
        book.save()
        return HttpResponseRedirect(reverse('book_catalog:show', args=(book.id,)))

    context = {'form': form}
    return render(request, "add.html", context)

def book_edit(request, id_buku):
    book = Book.objects.get(pk = id_buku)

    form = BookForm(request.POST or None, instance=book)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('book_catalog:show', args=(book.id,)))

    context = {'form': form}
    return render(request, "edit.html", context)
    
def book_delete(request, id_buku):
    book = Book.objects.get(id=id_buku)
    book.delete()
    return HttpResponseRedirect('/book/')