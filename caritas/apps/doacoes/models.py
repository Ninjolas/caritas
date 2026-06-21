from django.db import models
from apps.accounts.models import Usuario
from apps.estoque.models import CATEGORIA_CHOICES


class Doacao(models.Model):
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='doacoes'
    )
    doador = models.CharField(max_length=200)
    data = models.DateField()
    descricao = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doação de {self.doador} em {self.data}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Doação'
        verbose_name_plural = 'Doações'


class ItemDoacao(models.Model):
    doacao = models.ForeignKey(Doacao, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(
        'estoque.ProdutoCatalogo', on_delete=models.PROTECT,
        null=True, blank=True, related_name='itens_doacao'
    )
    nome = models.CharField(max_length=200, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, blank=True)
    quantidade = models.IntegerField()
    unidade = models.CharField(max_length=50, default='unidade')
    data_validade = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.produto:
            self.nome = self.produto.nome
            self.categoria = self.produto.categoria
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade} {self.unidade} de {self.nome or '—'}"
