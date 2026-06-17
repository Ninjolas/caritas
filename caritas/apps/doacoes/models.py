from django.db import models
from apps.accounts.models import Usuario
from apps.estoque.models import ItemEstoque


class Doacao(models.Model):
    paroquia = models.CharField(max_length=100)
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
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=ItemEstoque.CATEGORIA_CHOICES)
    categoria_outro = models.CharField(max_length=100, blank=True, default='')
    quantidade = models.IntegerField()
    unidade = models.CharField(max_length=50, default='unidade')
    data_validade = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantidade} {self.unidade} de {self.nome}"
