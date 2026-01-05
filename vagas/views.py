from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from .models import Vaga
from .forms import VagaForm


class ListaVagasView(ListView):
    model = Vaga
    template_name = 'vagas/lista_vagas.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        return Vaga.objects.filter(ativa=True).order_by('-criada_em')
    
class CriarVagaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'vagas/criar_vaga.html'
    success_url = reverse_lazy('vagas:lista_vagas')

    def test_func(self):
        return self.request.user.is_superuser

class TelaVagasView(LoginRequiredMixin, FormMixin, ListView):
    model = Vaga
    template_name = 'vagas/tela_vagas.html'
    context_object_name = 'vagas'
    form_class = VagaForm
    success_url = reverse_lazy('vagas:tela_vagas')

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                "Você não tem permissão para criar vagas."
            )

        self.object_list = self.get_queryset()
        form = self.get_form()

        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.criada_por = request.user
            vaga.save()
            return redirect(self.success_url)

        return self.render_to_response(
            self.get_context_data(form=form)
        )
