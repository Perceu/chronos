from django import forms
from django.contrib.auth.models import User
from chronos.usuarios.models import Usuario
from chronos.core.context import get_empresa
from django.db import transaction

class UsuarioCreateForm(forms.ModelForm):

    username = forms.CharField(label="Login")
    primeiro_nome = forms.CharField(label="Primeiro Nome")
    ultimo_nome = forms.CharField(label="Último Nome")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["role"]
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["username"].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.user.email
            self.fields["primeiro_nome"].initial = self.instance.user.first_name
            self.fields["ultimo_nome"].initial = self.instance.user.last_name
            self.fields["password"].widget = forms.HiddenInput()
            self.fields["password"].required = False


    def save(self, commit=True):
        with transaction.atomic():
            usuario = super().save(commit=False)
            if usuario.pk:
                user = usuario.user
            else:
                user = User()

            user.username = self.cleaned_data["username"]
            user.email = self.cleaned_data["email"]
            user.first_name = self.cleaned_data["primeiro_nome"]
            user.last_name = self.cleaned_data["ultimo_nome"]   
            password = self.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()
            usuario.user = user
            usuario.empresa = get_empresa()

            if commit:
                usuario.save()
            return usuario