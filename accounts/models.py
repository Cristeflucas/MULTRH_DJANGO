from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
import re


class Plano(models.Model):
    nome = models.CharField(max_length=100)
    duracao_dias = models.IntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
    
class Assinatura(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    ativa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.plano and not self.data_fim:
            self.data_fim = self.data_inicio + timedelta(days=self.plano.duracao_dias)
        super().save(*args, **kwargs)
    def expirou(self):
        return timezone.now() > self.data_fim
    
    def __str__(self):
        return self.user.get_full_name() or self.user.email


def validate_cpf(value):
    cpf = value

    numeros = [int(d) for d in cpf if d.isdigit()]

    if len(numeros) != 11:
        raise ValidationError("CPF inválido")

    if numeros == numeros[::-1]:
        raise ValidationError("CPF inválido")

    soma = sum(a * b for a, b in zip(numeros[:9], range(10, 1, -1)))
    digito = (soma * 10 % 11) % 10
    if numeros[9] != digito:
        raise ValidationError("CPF inválido")

    soma = sum(a * b for a, b in zip(numeros[:10], range(11, 1, -1)))
    digito = (soma * 10 % 11) % 10
    if numeros[10] != digito:
        raise ValidationError("CPF inválido")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[validate_cpf]
    )

    def __str__(self):
        return self.user.get_full_name()
