from django.shortcuts import redirect
from django.urls import reverse
from .models import Assinatura


PUBLIC_PATHS = [
    '/',
    '/index/',
    '/vagas/',
    '/accounts/login/',
    '/accounts/cadastro/',
    '/accounts/checkout/',
    '/logout/',
]


class AssinaturaAtivaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.checkout_url = reverse('accounts:checkout')

    def __call__(self, request):
        # 🔹 Libera arquivos estáticos e favicon
        if request.path.startswith('/static/') or request.path == '/favicon.ico':
            return self.get_response(request)

        # 🔹 Libera rotas públicas
        if request.path in PUBLIC_PATHS:
            return self.get_response(request)

        # 🔹 Protege apenas rotas privadas
        if request.user.is_authenticated:
            try:
                assinatura = Assinatura.objects.get(user=request.user, ativa=True)

                # assinatura expirada
                if assinatura.expirou():
                    assinatura.ativa = False
                    assinatura.save()
                    return redirect(self.checkout_url)

            except Assinatura.DoesNotExist:
                return redirect(self.checkout_url)

        return self.get_response(request)
