from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogoutView
app_name = "accounts"

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]