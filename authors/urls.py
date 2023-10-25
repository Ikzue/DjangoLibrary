from django.urls import path

from .views import AuthorListView, AuthorDetailView, AuthorCreateView, AuthorUpdateView, AuthorDeleteView

app_name = "authors"

urlpatterns = [
    path('', AuthorListView.as_view(extra_context={"title": "Author List"}), name='list'),
    path('details/<int:pk>/', AuthorDetailView.as_view(extra_context={"title": "Author Details"}), name='details'),
    path('create/', AuthorCreateView.as_view(extra_context={"title": "Create Author"}), name='create'),
    path('update/<int:pk>/', AuthorUpdateView.as_view(extra_context={"title": "Update Author"}), name='update'),
    path('delete/<int:pk>/', AuthorDeleteView.as_view(extra_context={"title": "Delete Author"}), name='delete'),
]