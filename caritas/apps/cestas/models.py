from django.db import models
from apps.accounts.models import Usuario
from apps.familias.models import Familia


class CestaPronta(models.Model):
    ORIGEM_CHOICES = [
        ('montagem', 'Montagem interna'),
        ('doacao', 'Doação recebida'),
    ]

    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.CASCADE,
        null=True, blank=True, related_name='cestas_prontas'
    )
    quantidade = models.IntegerField(default=0)
    origem = models.CharField(max_length=10, choices=ORIGEM_CHOICES)
    data = models.DateField()
    observacao = models.TextField(blank=True)
    registrado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name='cestas_registradas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantidade} cesta(s) — {self.get_origem_display()} em {self.data}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Entrada de Cestas Prontas'
        verbose_name_plural = 'Entradas de Cestas Prontas'


class ItemMontagem(models.Model):
    cesta_pronta = models.ForeignKey(CestaPronta, on_delete=models.CASCADE, related_name='itens_usados')
    item_estoque = models.ForeignKey(
        'estoque.ItemEstoque', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='usos_montagem'
    )
    item_nome = models.CharField(max_length=200, blank=True)
    quantidade_total = models.IntegerField(
        help_text='Quantidade total retirada do estoque para todas as cestas'
    )

    def __str__(self):
        nome = self.item_nome or (self.item_estoque.nome if self.item_estoque else '—')
        return f"{self.quantidade_total}x {nome}"


class EntregaCesta(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='cestas_recebidas')
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='entregas_cesta'
    )
    quantidade = models.IntegerField(default=1)
    data = models.DateField()
    observacao = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrega de {self.quantidade} cesta(s) para {self.familia.responsavel_nome} em {self.data}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Entrega de Cesta'
        verbose_name_plural = 'Entregas de Cestas'
