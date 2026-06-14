from django.db import models
from django.db.models import Sum
from apps.accounts.models import Usuario


class BrechoEvento(models.Model):
    STATUS_CHOICES = [
        ('planejado', 'Planejado'),
        ('em_andamento', 'Em andamento'),
        ('encerrado', 'Encerrado'),
    ]

    nome = models.CharField(max_length=200)
    paroquia = models.CharField(max_length=100)
    data = models.DateField()
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejado')
    criado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='breches_criados')
    criado_em = models.DateTimeField(auto_now_add=True)

    def total_vendas(self):
        return self.vendas.aggregate(total=Sum('valor_total'))['total'] or 0

    def total_pecas_vendidas(self):
        return self.vendas.aggregate(total=Sum('quantidade'))['total'] or 0

    def __str__(self):
        return f"{self.nome} — {self.paroquia} ({self.data})"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Evento de Brechó'
        verbose_name_plural = 'Eventos de Brechó'


class VendaBrecho(models.Model):
    evento = models.ForeignKey(BrechoEvento, on_delete=models.CASCADE, related_name='vendas')
    item_estoque = models.ForeignKey(
        'estoque.ItemEstoque',
        on_delete=models.PROTECT,
        related_name='vendas_brecho',
        limit_choices_to={'categoria': 'roupa'},
    )
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade}x {self.item_estoque.nome} — R$ {self.valor_total}"

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Venda do Brechó'
        verbose_name_plural = 'Vendas do Brechó'
