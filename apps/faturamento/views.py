from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView

from apps.faturamento.forms import NotaCobrancaForm
from apps.faturamento.models import NotaCobranca


class NotaCobrancaCreate(CreateView):
    model = NotaCobranca
    form_class = NotaCobrancaForm

    def get_form_kwargs(self):
        kwargs = super(NotaCobrancaCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        nota = form.save(commit=False)
        nota.empresa = self.request.user.usuario.empresa
        nota.data_inclusao = timezone.now()
        nota.save()
        return super(NotaCobrancaCreate, self).form_valid(form)
