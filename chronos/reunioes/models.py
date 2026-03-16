from django.db import models
from chronos.projetos.models import Projeto
from chronos.empresas.baseModel import EmpresaModel

# Create your models here.
class Reuniao(EmpresaModel):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, default='')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    inicio = models.DateTimeField(default=None, null=True)
    fim = models.DateTimeField(default=None, null=True)