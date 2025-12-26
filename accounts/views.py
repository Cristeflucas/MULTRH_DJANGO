from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render
from .models import Profile
from .models import Plano


def checkout(request):
    if "cadastro" not in request.session:
        return redirect("cadastro")
    
    planos = Plano.objects.all()
    return render(request, "accounts/checkout.html", {"planos": planos})

def confirmar_pagamento(request):
    dados = request.session.get("cadastro")
    plano_id = request.POST.get("plano_id")

    if not dados or not plano_id:
        return redirect("cadastro")
    
    plano = get_object_or_404(Plano, id=plano_id)

    user = User.objects.create_user(
        username=dados["email"],
        email=dados["email"],
        password=dados["password"],
        first_name=dados["nome"].split()[0],
        last_name=" ".join(dados["nome"].split()[1:]),
    )

    profile = Profile.objects.create(
        user=user,
        cpf=dados["cpf"]
    )

    login(request, user)
    del request.session["cadastro"]

    messages.success(request, "Pagamento confirmado! Conta criada com sucesso.")
    return redirect("index")



def escolher_plano(request):
    planos = Plano.objects.all()
    return render(request, "accounts/planos.html", {"planos": planos})

def login_modal(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Email ou senha inválidos.")
        
        return redirect("index")

def logout_view(request):
    logout(request)
    return redirect("index")

def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get("nome_completo")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "As senhas não coincidem.")
            return redirect("cadastro")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado.")
            return redirect("cadastro")

        if Profile.objects.filter(cpf=cpf).exists():
            messages.error(request, "CPF já cadastrado.")
            return redirect("cadastro")

        request.session["cadastro"] = {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "password": password
        }

        return redirect("checkout")

    return render(request, "accounts/cadastro.html")

