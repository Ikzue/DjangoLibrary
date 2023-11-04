from datetime import datetime
from django import forms

class CustomDateField(forms.DateField):
    def to_python(self, value):
        for fmt in ('%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        return super().to_python(value)