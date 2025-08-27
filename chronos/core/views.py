from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.models import User

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


class ChronosLoginView(LoginView):
    pass


class ChronosLogoutView(LogoutView):
    template_name="registration/my_logged_out.html"
    pass


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')


class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')
