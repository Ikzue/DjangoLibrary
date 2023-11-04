from django.db import models
from django_countries.fields import CountryField

class Author(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    country = CountryField()
    birth_date = models.DateField()

    def __str__(self):
        author = self.last_name
        if self.middle_name: author += f" {self.middle_name}" 
        if self.first_name: author += f" {self.first_name}" 
        return author
