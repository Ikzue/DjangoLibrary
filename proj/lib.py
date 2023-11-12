from datetime import datetime
import string, random

from django import forms

class CustomDateField(forms.DateField):
    def to_python(self, value):
        for fmt in ('%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                pass
        return super().to_python(value)
    
def random_field(N):
    chars = string.ascii_letters + string.digits + ' '
    return "".join(random.choices(chars, k=N)).strip()

def random_date():
    return datetime.strptime(
        f"{random.randint(1,28)}/{random.randint(1,12)}/{random.randint(1900, 2023)}",
        "%d/%m/%Y"
    )
