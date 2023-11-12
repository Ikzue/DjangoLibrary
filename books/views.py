from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book
from .forms import BookForm


class BookListView(ListView):
    template_name = "book-list.html"
    queryset = Book.objects.all()


class BookDetailView(DetailView):
    template_name = "book-details.html"
    model = Book


class BookCreateView(LoginRequiredMixin, FormView):
    template_name = "book-create.html"
    form_class = BookForm

    def form_valid(self, form):
        book = form.save()
        return redirect('books:details', pk=book.id)     


class BookUpdateView(LoginRequiredMixin, FormView):
    template_name = "book-update.html"
    form_class = BookForm

    def get_context_data(self, **kwargs):  # GET
        if "form" not in kwargs:
            book = get_object_or_404(Book, pk=self.kwargs["pk"])
            kwargs["form"] = self.form_class(instance=book)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):  # POST
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        form = self.form_class(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books:details', pk=book.id) 
        return render(request, self.template_name, {'form': form})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "book-delete.html"
    model = Book
    success_url = reverse_lazy('books:list')   
