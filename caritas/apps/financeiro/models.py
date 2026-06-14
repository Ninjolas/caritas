from django.db import models
from apps.accounts.models import Usuario


class MovimentacaoFinanceira(models.Model):
    TIPO_CHOICES = [
        ('entrada_doacao', 'Entrada — Doação espontânea'),
        ('entrada_vendas', 'Entrada — Receita de vendas'),
        ('saida_insumos', 'Saída — Compra de insumos'),
        ('saida_projeto', 'Saída — Aquisição para projeto'),
        ('saida_doacao_terceiros', 'Saída — Doação a projeto de terceiros'),
    ]
    ORIGEM_CHOICES = [
        ('diocese', 'Diocese'),
        ('paroquia', 'Paróquia'),
    ]

    origem = models.CharField(max_length=10, choices=ORIGEM_CHOICES)
    paroquia = models.CharField(max_length=100, blank=True, help_text='Preencher apenas se origem = Paróquia')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    descricao = models.TextField()
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def eh_entrada(self):
        return self.tipo.startswith('entrada')

    def __str__(self):
        return f"{self.get_tipo_display()} — R$ {self.valor} em {self.data}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Movimentação Financeira'
        verbose_name_plural = 'Movimentações Financeiras'
