from django.shortcuts import render

# Create your views here.

# menampilkan page detail buku
def detail_buku(request, id_buku):
    return render(request, 'modul_data_buku/detail_buku.html')