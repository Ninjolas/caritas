from django.db import models
from apps.accounts.models import Usuario


class ItemEstoque(models.Model):
    CATEGORIA_CHOICES = [
        ('alimento', 'Alimento'),
        ('roupa', 'Roupa'),
        ('medicamento', 'Medicamento'),
        ('outro', 'Outro'),
    ]

    paroquia = models.CharField(max_length=100)
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    categoria_outro = models.CharField(max_length=100, blank=True, default='')
    quantidade = models.IntegerField(default=0)
    unidade = models.CharField(max_length=50, default='unidade')
    validade = models.DateField(null=True, blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.quantidade <= 0:
            try:
                self.delete()
            except Exception:
                pass

    def __str__(self):
        return f"{self.nome} ({self.paroquia})"

    class Meta:
        ordering = ['validade', 'nome']
        verbose_name = 'Item do Estoque'
        verbose_name_plural = 'Itens do Estoque'
