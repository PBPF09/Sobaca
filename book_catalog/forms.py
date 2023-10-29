from django.forms import ModelForm
from book_catalog.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review']