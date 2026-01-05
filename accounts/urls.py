from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import cadastro

app_name = 'accounts'

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('checkout/', views.checkout, name='checkout'),
    path('planos/', views.escolher_plano, name='escolher_plano'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])