from django.db import models


class Checklist(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

class ChecklistItem(models.Model):
    descricao = models.TextField()
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)