from django import forms
from search_book.models import Request

class RequestForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'cols':30, 'rows':1 , 'placeholder':"Title Book"}))
    author = forms.CharField(widget=forms.Textarea(attrs={'cols':30, 'rows':1, 'placeholder':"Author"}))
    year = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "Year"}))
    class Meta:
        model = Request
        fields = ['title', 'author', 'year']