from django.db import models
from apps.accounts.models import Usuario
from apps.familias.models import Familia


class Atendimento(models.Model):
    TIPO_CHOICES = [
        ('assistencia_social', 'Assistência Social'),
        ('doacao_alimentos', 'Doação de Alimentos'),
        ('doacao_roupas', 'Doação de Roupas'),
        ('encaminhamento', 'Encaminhamento'),
        ('visita_domiciliar', 'Visita Domiciliar'),
        ('outro', 'Outro'),
    ]

    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='atendimentos')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    data = models.DateField()
    descricao = models.TextField()
    paroquia = models.CharField(max_length=100)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atendimento {self.get_tipo_display()} — {self.familia.responsavel_nome} ({self.data})"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'
