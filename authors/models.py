from django.db import models

class Author(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=50)
    birth_date = models.DateField()