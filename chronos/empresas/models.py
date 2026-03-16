from django.db import models

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    domain = models.CharField(max_length=200, default='localhost:8000')

    def __str__(self):
        return self.nome