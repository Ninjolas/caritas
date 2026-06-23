from django.db import models
from apps.accounts.models import Usuario
from apps.familias.models import Familia


class ModeloCesta(models.Model):
    nome = models.CharField(max_length=200)
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='modelos_cesta'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Modelo de Cesta'
        verbose_name_plural = 'Modelos de Cesta'

    def __str__(self):
        return self.nome


class ModeloItemCesta(models.Model):
    modelo = models.ForeignKey(ModeloCesta, on_delete=models.CASCADE, related_name='itens')
    nome = models.CharField(max_length=200)
    quantidade = models.IntegerField(default=1)
    unidade = models.CharField(max_length=50, default='unidade')

    def __str__(self):
        return f"{self.quantidade} {self.unidade} de {self.nome}"


class CestaRecebida(models.Model):
    data = models.DateField()
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cestas_recebidas'
    )
    doador_nome = models.CharField(max_length=200, blank=True, verbose_name='Doador')
    observacao = models.TextField(blank=True, verbose_name='Observacao')
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Cesta Recebida'
        verbose_name_plural = 'Cestas Recebidas'

    def __str__(self):
        return f"Cesta recebida em {self.data} — {self.doador_nome or 'Anonimo'}"


class ItemCestaRecebida(models.Model):
    cesta = models.ForeignKey(CestaRecebida, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(
        'estoque.ProdutoCatalogo', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    nome = models.CharField(max_length=200)
    quantidade = models.IntegerField()
    unidade = models.CharField(max_length=50, default='unidade')
    validade = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantidade} {self.unidade} de {self.nome}"


class CestaEntregue(models.Model):
    data = models.DateField()
    familia = models.ForeignKey(
        Familia, on_delete=models.CASCADE, related_name='cestas_entregues'
    )
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cestas_entregues'
    )
    modelo_usado = models.ForeignKey(
        ModeloCesta, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Modelo de cesta'
    )
    observacao = models.TextField(blank=True, verbose_name='Observacao')
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Cesta Entregue'
        verbose_name_plural = 'Cestas Entregues'

    def __str__(self):
        return f"Cesta para {self.familia.responsavel_nome} em {self.data}"


class ItemCestaEntregue(models.Model):
    cesta = models.ForeignKey(CestaEntregue, on_delete=models.CASCADE, related_name='itens')
    item_estoque = models.ForeignKey(
        'estoque.ItemEstoque', on_delete=models.SET_NULL,
        null=True, related_name='usos_cesta'
    )
    item_nome = models.CharField(max_length=200)
    item_unidade = models.CharField(max_length=50, default='unidade')
    quantidade = models.IntegerField()

    def __str__(self):
        return f"{self.quantidade}x {self.item_nome}"
