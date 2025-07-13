from django.db import models
from django.urls import reverse


# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=250)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True, default="")

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("cliente-detail", kwargs={"pk": self.pk})
