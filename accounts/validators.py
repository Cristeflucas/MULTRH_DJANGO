import re
from django.core.exceptions import ValidationError

def validate_cpf(value):
    cpf = value

    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        raise ValidationError("CPF deve estar no formato XXX.XXX.XXX-XX")

    numeros = [int(d) for d in cpf if d.isdigit()]

    if len(numeros) != 11:
        raise ValidationError("CPF inválido")

    if len(set(numeros)) == 1:
        raise ValidationError("CPF inválido")

    soma = sum(a * b for a, b in zip(numeros[:9], range(10, 1, -1)))
    digito1 = (soma * 10 % 11) % 10
    if numeros[9] != digito1:
        raise ValidationError("CPF inválido")

    soma = sum(a * b for a, b in zip(numeros[:10], range(11, 1, -1)))
    digito2 = (soma * 10 % 11) % 10
    if numeros[10] != digito2:
        raise ValidationError("CPF inválido")
