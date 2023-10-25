from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView, DeleteView, UpdateView
from django.db.models import ProtectedError
# Create your views here.
from .models import Author
from .forms import AuthorForm
class AuthorListView(ListView):
    template_name = "author-list.html"
    queryset = Author.objects.all()

class AuthorDetailView(DetailView):
    template_name = "author-details.html"
    model = Author


class AuthorCreateView(FormView):
    template_name = "author-create.html"
    form_class = AuthorForm

    def form_valid(self, form):
        author = form.save()
        return redirect('authors:details', pk=author.id)    


class AuthorUpdateView(FormView):
    template_name = "author-update.html"
    form_class = AuthorForm

    def get_context_data(self, **kwargs):  # GET
        if "form" not in kwargs:
            author = get_object_or_404(Author, pk=self.kwargs["pk"])
            kwargs["form"] = self.form_class(instance=author)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):  # POST
        author = get_object_or_404(Author, pk=self.kwargs["pk"])
        form = self.form_class(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            return redirect('authors:details', pk=author.id) 
        return render(request, self.template_name, {'form': form})


class AuthorDeleteView(DeleteView):
    template_name = "author-delete.html"
    model = Author
    success_url = reverse_lazy('authors:list')   

    def form_valid(self, request, *args, **kwargs):
        pk = self.object.id
        try:
            self.object.delete()
        except ProtectedError as e:
            protected_objects = [f"\n{str(protected_obj)}" for protected_obj in e.protected_objects]
            return HttpResponse(f"Couldn't delete this author, some fields were protected: {protected_objects}")
        return redirect('authors:list') 