from django.db import models
from apps.accounts.models import Usuario
from apps.familias.models import Familia

TIPOS_COM_ITENS = ['doacao_roupas', 'doacao_cesta_basica']


class Atendimento(models.Model):
    TIPO_CHOICES = [
        ('assistencia_social', 'Assistência Social'),
        ('doacao_roupas', 'Doação de Roupas'),
        ('doacao_cesta_basica', 'Doação de Cesta Básica'),
        ('encaminhamento', 'Encaminhamento'),
        ('visita_domiciliar', 'Visita Domiciliar'),
        ('outro', 'Outro'),
    ]

    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='atendimentos')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    data = models.DateField()
    descricao = models.TextField(blank=True)
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='atendimentos'
    )
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atendimento {self.get_tipo_display()} — {self.familia.responsavel_nome} ({self.data})"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'


class ItemAtendimento(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, related_name='itens')
    item_estoque = models.ForeignKey(
        'estoque.ItemEstoque', on_delete=models.SET_NULL, null=True, related_name='usos_atendimento'
    )
    item_nome = models.CharField(max_length=200)
    item_unidade = models.CharField(max_length=50, default='unidade')
    quantidade = models.IntegerField()

    def __str__(self):
        return f"{self.quantidade}x {self.item_nome}"
