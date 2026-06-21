from django.db import models
from apps.accounts.models import Usuario

CATEGORIA_CHOICES = [
    ('alimento', 'Alimento'),
    ('roupa', 'Roupa'),
    ('calcado', 'Calçado'),
    ('medicamento', 'Medicamento'),
    ('outro', 'Outro'),
]

GENERO_CHOICES = [
    ('masculino', 'Masculino'),
    ('feminino', 'Feminino'),
    ('infantil', 'Infantil'),
    ('unissex', 'Unissex'),
]

TAMANHO_ROUPA_CHOICES = [
    ('pp', 'PP'), ('p', 'P'), ('m', 'M'),
    ('g', 'G'), ('gg', 'GG'), ('xgg', 'XGG'), ('unico', 'Único'),
]

TIPO_CALCADO_CHOICES = [
    ('tenis', 'Tênis'),
    ('sapato', 'Sapato'),
    ('sandalia', 'Sandália'),
    ('bota', 'Bota'),
    ('chinelo', 'Chinelo'),
    ('sapatilha', 'Sapatilha'),
    ('outro', 'Outro'),
]


class ProdutoCatalogo(models.Model):
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.CASCADE,
        null=True, blank=True, related_name='catalogo_produtos'
    )
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    # Campos de roupa
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=True)
    tamanho = models.CharField(max_length=10, choices=TAMANHO_ROUPA_CHOICES, blank=True)
    # Campos de calçado (tipo = subcategoria)
    tipo_calcado = models.CharField(max_length=20, choices=TIPO_CALCADO_CHOICES, blank=True)
    tamanho_calcado = models.CharField(max_length=10, blank=True, help_text='Ex: 38, 39, 40')
    categoria_outro = models.CharField(max_length=100, blank=True, default='', verbose_name='Descrição (outro)')
    unidade_padrao = models.CharField(max_length=50, default='unidade')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.nome = ' '.join(self.nome.strip().split()).title()
        super().save(*args, **kwargs)

    def __str__(self):
        partes = [self.nome]
        if self.genero:
            partes.append(self.get_genero_display())
        if self.tamanho:
            partes.append(self.get_tamanho_display())
        if self.tipo_calcado:
            partes.append(self.get_tipo_calcado_display())
        if self.tamanho_calcado:
            partes.append(f'nº {self.tamanho_calcado}')
        return ' — '.join(partes)

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

        # Merge com item existente de mesmo produto, paróquia e validade
        if not self.pk and self.produto:
            existente = ItemEstoque.objects.filter(
                produto=self.produto,
                paroquia=self.paroquia,
                validade=self.validade,
            ).first()
            if existente:
                existente.quantidade += self.quantidade
                existente.save()
                self.pk = existente.pk
                return

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
