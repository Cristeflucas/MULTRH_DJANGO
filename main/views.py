from django.shortcuts import render
from vagas.models import Vaga

def index(request):
    vagas = Vaga.objects.all()[:6]
    return render(request, 'main/index.html', {'vagas': vagas})

def base(request):
    return render(request, 'templates/base.html')
