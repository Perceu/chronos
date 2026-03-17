from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from chronos.usuarios.models import Usuario

class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [UsuarioInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)