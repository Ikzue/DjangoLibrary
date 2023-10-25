from django.urls import path

from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

app_name = "books"

urlpatterns = [
    path('', BookListView.as_view(extra_context={"title": "Book List"}), name='list'),
    path('details/<int:pk>/', BookDetailView.as_view(extra_context={"title": "Book Details"}), name='details'),
    path('create/', BookCreateView.as_view(extra_context={"title": "Create Book"}), name='create'),
    path('update/<int:pk>/', BookUpdateView.as_view(extra_context={"title": "Update Book"}), name='update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(extra_context={"title": "Delete Book"}), name='delete'),
]