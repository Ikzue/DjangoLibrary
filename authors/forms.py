from datetime import datetime

from proj.lib import CustomDateField
from django import forms
from .models import Author



class AuthorForm(forms.ModelForm):
    birth_date = CustomDateField()
    class Meta:
        model = Author
        fields = ["last_name", "first_name", "middle_name", "country", "birth_date",]