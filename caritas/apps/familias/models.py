import uuid

from django.db import models

from apps.accounts.models import Usuario


class Familia(models.Model):
    ESCOLARIDADE_CHOICES = [
        ('fundamental_incompleto', 'Fundamental Incompleto'),
        ('fundamental_completo', 'Fundamental Completo'),
        ('medio_incompleto', 'Médio Incompleto'),
        ('medio_completo', 'Médio Completo'),
        ('superior', 'Superior'),
    ]

    id_interno = models.CharField(max_length=50, unique=True, blank=True)
    possui_cpf = models.BooleanField(default=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    responsavel_nome = models.CharField(max_length=200)
    nacionalidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=300)
    telefone = models.CharField(max_length=20, blank=True)
    escolaridade = models.CharField(max_length=30, choices=ESCOLARIDADE_CHOICES)
    ocupacao = models.CharField(max_length=100, blank=True)
    local_trabalho = models.CharField(max_length=200, blank=True)
    situacao_vulnerabilidade = models.TextField(blank=True)
    renda_familiar = models.DecimalField(max_digits=10, decimal_places=2)
    bolsa_familia = models.BooleanField(default=False)
    valor_beneficio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qtd_pessoas = models.IntegerField()
    qtd_criancas = models.IntegerField(default=0)
    paroquia_responsavel = models.CharField(max_length=100)
    criado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name='familias_cadastradas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.possui_cpf and not self.id_interno:
            prefixo = self.paroquia_responsavel[:3].upper() if self.paroquia_responsavel else 'SEM'
            self.id_interno = f'INT-{prefixo}-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Família'
        verbose_name_plural = 'Famílias'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.responsavel_nome} ({self.id_interno})'


class Dependente(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('outro', 'Outro'),
    ]

    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='dependentes')
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)

    class Meta:
        verbose_name = 'Dependente'
        verbose_name_plural = 'Dependentes'

    def __str__(self):
        return f'{self.nome} ({self.idade} anos)'
