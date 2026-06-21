from django.db import models
from apps.accounts.models import Usuario

CATEGORIA_CHOICES = [
    ('alimento', 'Alimento'),
    ('roupa', 'Roupa'),
    ('medicamento', 'Medicamento'),
    ('outro', 'Outro'),
]


class ProdutoCatalogo(models.Model):
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.CASCADE,
        null=True, blank=True, related_name='catalogo_produtos'
    )
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    unidade_padrao = models.CharField(max_length=50, default='unidade')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.nome = ' '.join(self.nome.strip().split()).title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['categoria', 'nome']
        unique_together = [['nome', 'paroquia']]
        verbose_name = 'Produto'
        verbose_name_plural = 'Catálogo de Produtos'


class ItemEstoque(models.Model):
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.CASCADE,
        null=True, blank=True, related_name='itens_estoque'
    )
    produto = models.ForeignKey(
        ProdutoCatalogo, on_delete=models.PROTECT,
        null=True, blank=True, related_name='itens_estoque'
    )
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    categoria_outro = models.CharField(max_length=100, blank=True, default='')
    quantidade = models.IntegerField(default=0)
    unidade = models.CharField(max_length=50, default='unidade')
    validade = models.DateField(null=True, blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.produto:
            self.nome = self.produto.nome
            self.categoria = self.produto.categoria
        super().save(*args, **kwargs)
        if self.quantidade <= 0:
            try:
                self.delete()
            except Exception:
                pass

    def esta_vencido(self):
        from datetime import date
        if self.validade:
            return self.validade < date.today()
        return False

    def vence_em_breve(self):
        from datetime import date, timedelta
        if self.validade:
            return date.today() <= self.validade <= date.today() + timedelta(days=7)
        return False

    def __str__(self):
        return f"{self.nome} ({self.paroquia or 'sem paróquia'})"

    class Meta:
        ordering = ['validade', 'nome']
        verbose_name = 'Item do Estoque'
        verbose_name_plural = 'Itens do Estoque'
