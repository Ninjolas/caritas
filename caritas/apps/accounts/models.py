from django.contrib.auth.models import AbstractUser
from django.db import models


class Paroquia(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = 'Paróquia'
        verbose_name_plural = 'Paróquias'


class Usuario(AbstractUser):
    PERFIL_CHOICES = [
        ('voluntario', 'Voluntário'),
        ('coordenador', 'Coordenador'),
        ('administrador', 'Administrador'),
        ('coordenador_bazar', 'Coordenador do Bazar'),
        ('voluntario_bazar', 'Voluntário do Bazar'),
    ]

    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='voluntario')
    paroquia = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name() or self.username
