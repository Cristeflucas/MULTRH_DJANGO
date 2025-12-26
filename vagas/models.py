from django.db import models

# Create your models here.

class Vaga(models.Model):

    TIPO_CHOICES = [
        ('CLT', 'CLT'),
        ('PJ', 'PJ'),
        ('Freelancer', 'Freelancer'),
        ('Estágio', 'Estágio'),
    ]

    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} na {self.empresa}"