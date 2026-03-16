from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from chronos.usuarios.forms import UsuarioCreateForm 
from chronos.usuarios.models import Usuario    


# Create your views here.
class UserListView(ListView):
    model = Usuario
    template_name = 'usuarios/user_list.html'


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('user-list')


class UserCreateView(CreateView):
    form_class = UsuarioCreateForm
    template_name = 'usuarios/user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        return valid_form


class UserUpdateView(UpdateView):
    model = Usuario
    form_class  = UsuarioCreateForm
    template_name = 'usuarios/user_form.html'
    success_url = reverse_lazy('user-list')


# class UserPasswordView(UpdateView):
#     model = Usuario
#     form_class = UserPasswordModelForm
#     template_name = 'usuarios/user_form.html'
#     success_url = reverse_lazy('user-list')

#     def form_valid(self, form):
#         valid_form = super().form_valid(form)
#         self.object.set_password(form.cleaned_data['password'])
#         self.object.save()
#         return valid_form


class UserDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')