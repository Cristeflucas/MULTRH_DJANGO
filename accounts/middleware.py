from django.shortcuts import redirect
from django.urls import reverse
from .models import Assinatura

class AssinaturaAtivaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                assinatura = Assinatura.objects.get(user=request.user, ativa=True)
                if assinatura.expirou():
                    assinatura.ativa = False
                    assinatura.save()
                    return redirect(reverse('accounts:escolher_plano'))
            except Assinatura.DoesNotExist:
                return redirect(reverse('accounts:escolher_plano'))

        response = self.get_response(request)
        return response