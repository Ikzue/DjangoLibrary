from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from books.models import Book

def home_page(request):
    template = loader.get_template("home.html")
    context = {"object_list": Book.objects.all().values_list('title', flat=True)}
    return HttpResponse(template.render(context))
