from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["author", "co_authors", "title", "isbn", "release_date", "description",]