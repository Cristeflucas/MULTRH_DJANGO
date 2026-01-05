from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'vagas'

urlpatterns = [
    path('', views.ListaVagasView.as_view(), name='lista_vagas'),
    path('tela/', views.TelaVagasView.as_view(), name='tela_vagas'),
    path('criar/', views.CriarVagaView.as_view(), name='criar_vaga'),
]
