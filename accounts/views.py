from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


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

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nome
            )

            profile = Profile(
                user=user,
                cpf=cpf
            )

            profile.full_clean()
            profile.save()

            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("index")

        except ValidationError as e:
            user.delete()
            messages.error(request, e.messages[0])
            return redirect("cadastro")

    return render(request, "accounts/cadastro.html")
