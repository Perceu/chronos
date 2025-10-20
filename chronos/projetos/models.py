from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from chronos.clientes.models import Cliente


class Projeto(models.Model):

    class Meta:
        ordering = ["pago", "nome"]
        permissions = [
            ("can_view_payment_info", "Can view payment information"),
        ]

    class StatusProjeto(models.TextChoices):
        ORCADO = "ORC", _("Orçado")
        CONTRATADO = "CTD", _("Contratado")
        ANDAMENTO = "AND", _("Andamento")
        CONCLUIDA = "CON", _("Concluido")
        BLOQUEADO = "BLO", _("Bloqueado")

    class StatusPagamento(models.TextChoices):
        ABERTO = "ABE", _("Aberto")
        CONCLUIDO = "CON", _("Concluido")
        PARCELADO = "PAR", _("Parcelado")
        ATRAZADO = "ATR", _("Atrasado")
        PERDIDO = "PER", _("Perdido")

    nome = models.CharField(max_length=200)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="projetos"
    )
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True)
    pago = models.BooleanField(default=False, null=True)
    pagamento = models.CharField(
        max_length=3,
        choices=StatusPagamento,
        default=StatusPagamento.ABERTO,
    )
    status = models.CharField(
        max_length=3,
        choices=StatusProjeto,
        default=StatusProjeto.ORCADO,
    )

    def __str__(self):
        return f"{self.nome} ({self.cliente.nome})"

    def get_absolute_url(self):
        return reverse("tarefa-projeto-list", kwargs={"projeto_id": self.pk})
