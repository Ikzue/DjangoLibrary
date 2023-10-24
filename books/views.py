from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from django.http import HttpResponse
# Create your views here.
from .models import Book
from .forms import BookForm

class BookListView(ListView):
    template_name = "list.html"
    queryset = Book.objects.all()
    extra_context={"title": "Custom Title"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Book List"
        return context

class BookDetailView(DetailView):
    template_name = "details.html"
    model = Book


class BookCreateView(FormView):
    template_name = "create.html"
    form_class = BookForm

    def form_valid(self, form):
        book = form.save()
        return redirect('book-details', pk=book.id)     


class BookUpdateView(FormView):
    template_name = "update.html"
    form_class = BookForm

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            try:
                book = Book.objects.get(id=self.kwargs["pk"])
                kwargs["form"] = self.form_class(instance=book)
            except Book.DoesNotExist:
                kwargs["error_book_not_found"] = f"Book {self.kwargs['pk']} does not exist"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        book = form.save()
        return redirect('book-details', pk=book.id) 


class BookDeleteView(DeleteView):
    template_name = "delete.html"
    model = Book
