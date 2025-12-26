from django.contrib import admin
from .models import Vaga

# Register your models here.

admin.site.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'local', 'tipo', 'ativa', 'criada_em')
    list_filter = ('tipo', 'ativa', 'criada_em')
    search_fields = ('titulo', 'empresa', 'local', 'descricao')

