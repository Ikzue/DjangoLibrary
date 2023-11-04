from django import forms
from .models import Book
from proj.lib import CustomDateField


class BookForm(forms.ModelForm):
    release_date = CustomDateField()
    class Meta:
        model = Book
        fields = ["author", "co_authors", "title", "isbn", "release_date", "description",]