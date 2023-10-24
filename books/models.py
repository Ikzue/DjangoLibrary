from django.db import models
from authors.models import Author

# Create your models here.
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    co_authors = models.ManyToManyField(Author, blank=True, related_name="coauthors")
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=17)
    release_date = models.DateField()
    description = models.TextField(null=True, blank=True)
