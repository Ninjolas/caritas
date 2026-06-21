from django.db import models
from apps.accounts.models import Usuario


class CategoriaBazar(models.Model):
    nome = models.CharField(max_length=100)
    pai = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='subcategorias'
    )
    ativa = models.BooleanField(default=True)

    def __str__(self):
        if self.pai:
            return f"{self.pai.nome} › {self.nome}"
        return self.nome

    def is_raiz(self):
        return self.pai is None

    class Meta:
        ordering = ['pai__nome', 'nome']
        verbose_name = 'Categoria do Bazar'
        verbose_name_plural = 'Categorias do Bazar'


class EmpresaParceira(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True)
    contato_nome = models.CharField(max_length=200, blank=True)
    contato_telefone = models.CharField(max_length=20, blank=True)
    contato_email = models.EmailField(blank=True)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = 'Empresa Parceira'
        verbose_name_plural = 'Empresas Parceiras'


class ItemEstoqueBazar(models.Model):
    TAMANHO_CHOICES = [
        ('pp', 'PP'), ('p', 'P'), ('m', 'M'),
        ('g', 'G'), ('gg', 'GG'), ('xgg', 'XGG'), ('unico', 'Único'),
    ]
    ESTADO_CHOICES = [
        ('novo', 'Novo'), ('bom', 'Bom estado'), ('regular', 'Regular'),
    ]

    descricao = models.CharField(max_length=200, blank=True)
    categoria = models.ForeignKey(
        CategoriaBazar, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='itens_estoque'
    )
    tamanho = models.CharField(max_length=10, choices=TAMANHO_CHOICES, default='unico')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='bom')
    quantidade = models.IntegerField(default=0)
    preco_sugerido = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        cat = str(self.categoria) if self.categoria else '—'
        return f"{self.descricao} — {self.get_tamanho_display()} ({self.quantidade} un.)"

    class Meta:
        ordering = ['categoria__nome', 'tamanho']
        verbose_name = 'Item do Estoque do Bazar'
        verbose_name_plural = 'Itens do Estoque do Bazar'


class EntradaBazar(models.Model):
    TIPO_DOADOR_CHOICES = [
        ('pessoa_fisica', 'Pessoa Física'),
        ('empresa', 'Empresa Parceira'),
    ]
    TIPO_ENTRADA_CHOICES = [
        ('doacao_item', 'Doação de itens'),
        ('doacao_financeira', 'Doação financeira'),
    ]

    tipo_entrada = models.CharField(max_length=20, choices=TIPO_ENTRADA_CHOICES)
    tipo_doador = models.CharField(max_length=20, choices=TIPO_DOADOR_CHOICES)
    doador_nome = models.CharField(max_length=200, blank=True)
    doador_contato = models.CharField(max_length=100, blank=True)
    empresa = models.ForeignKey(EmpresaParceira, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data = models.DateField()
    observacao = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='entradas_bazar')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        doador = self.empresa.nome if self.empresa else self.doador_nome
        return f"{self.get_tipo_entrada_display()} de {doador} em {self.data}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Entrada do Bazar'
        verbose_name_plural = 'Entradas do Bazar'


class ItemEntradaBazar(models.Model):
    entrada = models.ForeignKey(EntradaBazar, on_delete=models.CASCADE, related_name='itens')
    descricao = models.CharField(max_length=200, blank=True)
    categoria = models.ForeignKey(
        CategoriaBazar, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='itens_entrada'
    )
    tamanho = models.CharField(max_length=10, choices=ItemEstoqueBazar.TAMANHO_CHOICES, default='unico')
    estado = models.CharField(max_length=10, choices=ItemEstoqueBazar.ESTADO_CHOICES, default='bom')
    quantidade = models.IntegerField(default=1)
    preco_sugerido = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantidade}x {self.descricao}"


class Venda(models.Model):
    numero_operacao = models.CharField(max_length=20, unique=True, blank=True)
    item = models.ForeignKey(ItemEstoqueBazar, on_delete=models.PROTECT, related_name='vendas')
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    data = models.DateField()
    paroquia = models.ForeignKey(
        'accounts.Paroquia', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='vendas_bazar'
    )
    observacao = models.TextField(blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de {self.quantidade}x {self.item.descricao} em {self.data}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
