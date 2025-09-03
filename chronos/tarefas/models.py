from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from chronos.projetos.models import Projeto


class Tarefa(models.Model):
    class StatusTarefa(models.TextChoices):
        ABERTA = "ABE", _("Aberta")
        ANDAMENTO = "AND", _("Andamento")
        BLOQUEADA = "BLK", _("Bloqueada")
        CONCLUIDA = "CON", _("Concluida")

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, default="")
    projeto = models.ForeignKey(
        Projeto, on_delete=models.CASCADE, related_name="tarefas"
    )
    data_entrega = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=3,
        choices=StatusTarefa,
        default=StatusTarefa.ABERTA,
    )

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ["data_entrega"]

    @property
    def tempo_decorrido(self):
        total_segundos = 0
        for tempo in self.tempos.all():
            if not tempo.fim:
                continue
            diferenca = tempo.fim - tempo.inicio
            total_segundos += diferenca.total_seconds()

        return str(timedelta(seconds=total_segundos)).split(".")[0]

    @property
    def tempo_decorrido_segundos(self):
        total_segundos = 0
        for tempo in self.tempos.all():
            if not tempo.fim:
                continue
            diferenca = tempo.fim - tempo.inicio
            total_segundos += diferenca.total_seconds()

        return total_segundos

    @property
    def checklist_concluidas(self):
        return self.checklists.filter(concluido=True).count

    def get_absolute_url(self):
        return reverse("tarefa-detail", kwargs={"pk": self.pk})


class TarefaChecklist(models.Model):
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="checklists"
    )
    descricao = models.CharField(max_length=255, blank=True, null=True, default="")
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return str(self.descricao)

    def get_absolute_url(self):
        return reverse("tarefa-detail", kwargs={"pk": self.tarefa.pk})


class TarefaTempo(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="tempos")
    inicio = models.DateTimeField(blank=True, default=None)
    fim = models.DateTimeField(blank=True, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=200, null=True, blank=True, default="")

    def __str__(self):
        return f"{self.inicio} - {self.fim}"

    def get_absolute_url(self):
        return reverse("tarefa-detail", kwargs={"pk": self.tarefa.pk})
