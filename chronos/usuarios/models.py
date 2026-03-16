from django.db import models
from django.contrib.auth.models import User
from chronos.empresas.baseModel import EmpresaModel
from chronos.empresas.models import Empresa
# Create your models here.

class Usuario(EmpresaModel):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("manager", "Gerente"),
        ("user", "Colaborador"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="Função",
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
    )

    def __str__(self):
        return self.user.get_full_name()