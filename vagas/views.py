from django.shortcuts import render
from .models import Vaga
# Create your views here.

def lista_vagas(request):
    vagas = Vaga.objects.filter(ativa=True).order_by('-criada_em')
    return render(request, 'vagas/lista_vagas.html', {'vagas': vagas})

def tela_vagas(request):
    return render(request, 'vagas/tela_vagas.html')