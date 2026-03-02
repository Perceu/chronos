from django.db import models
from django.contrib.auth.models import User
from chronos.empresas.models import Empresa
# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()