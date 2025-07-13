from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from chronos.clientes.models import Cliente


class Projeto(models.Model):
    class StatusProjeto(models.TextChoices):
        ORCADO = "ORC", _("Orçado")
        CONTRATADO = "CTD", _("Contratado")
        ANDAMENTO = "AND", _("Andamento")
        CONCLUIDA = "CON", _("Concluido")

    nome = models.CharField(max_length=200)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="projetos"
    )
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True)
    pago = models.BooleanField(default=False, null=True)
    status = models.CharField(
        max_length=3,
        choices=StatusProjeto,
        default=StatusProjeto.ORCADO,
    )

    class Meta:
        ordering = ["pago","nome"]

    def __str__(self):
        return f"{self.nome} ({self.cliente.nome})"

    def get_absolute_url(self):
        return reverse("tarefa-projeto-list", kwargs={"projeto_id": self.pk})
