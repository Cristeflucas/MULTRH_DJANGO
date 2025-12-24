from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def base(request):
    return render(request, 'templates/base.html')
