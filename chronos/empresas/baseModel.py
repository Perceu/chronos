from django.db import models
from chronos.core.context import get_empresa

class EmpresaManager(models.Manager):

    def get_queryset(self):

        qs = super().get_queryset()
        empresa = get_empresa()

        if empresa:
            qs = qs.filter(empresa=empresa)

        return qs


class EmpresaModel(models.Model):

    empresa = models.ForeignKey(
        "empresas.Empresa", 
        on_delete=models.CASCADE, 
        default=None, 
        null=True
    )

    objects = EmpresaManager()

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.empresa_id:
            self.empresa = get_empresa()
        super().save(*args, **kwargs)