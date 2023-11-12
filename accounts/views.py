from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts-create.html'

    def form_valid(self, form):
        form.save()
        return redirect('books:list')

class UserLoginView(LoginView):
    template_name = 'accounts-login.html'

class UserLogoutView(LogoutView):
    template_name = 'accounts-logout.html'
    success_url = reverse_lazy('books:list')
