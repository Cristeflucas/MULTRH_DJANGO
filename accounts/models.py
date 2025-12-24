from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


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
