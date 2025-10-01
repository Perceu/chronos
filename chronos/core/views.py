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
    UpdateView
)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from chronos.core.forms import UserModelForm, UserPasswordModelForm

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


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('user-list')


class UserCreateView(CreateView):
    form_class = UserModelForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        return valid_form


class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')


class UserPasswordView(UpdateView):
    model = User
    form_class = UserPasswordModelForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        return valid_form


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')
