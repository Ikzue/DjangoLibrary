from django.urls import path

from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
urlpatterns = [
    path('', BookListView.as_view()),
    path('details/<int:pk>/', BookDetailView.as_view(extra_context={"title": "Book Details"}), name='book-details'),
    path('create/', BookCreateView.as_view(extra_context={"title": "Create Book"})),
    path('update/<int:pk>/', BookUpdateView.as_view(extra_context={"title": "Update Book"})),
    path('delete/<int:pk>/', BookDeleteView.as_view(extra_context={"title": "Delete Book"})),
]