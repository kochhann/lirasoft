from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import QuadroEquipamentoForm, ContratoForm, QuadroAcessorioForm
from .models import Contrato, QuadroEquipamentos, QuadroAcessorio
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)

class ContratoList(ListView):
    model = Contrato

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return Contrato.objects.filter(empresa=empresa_in, ativo=True)


class ContratoCreate(CreateView):
    model = Contrato
    form_class = ContratoForm

    def get_form_kwargs(self):
        kwargs = super(ContratoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        contrato = form.save(commit=False)
        contrato.empresa = self.request.user.usuario.empresa
        contrato.data_cadastro = timezone.now()
        contrato.save()
        return super(ContratoCreate, self).form_valid(form)

class ContratoEdit(UpdateView):
    model = Contrato
    fields = ['tipo', 'dataFim', 'valor', 'emitir_nota',
              'emitir_boleto', 'emitir_contabil', 'observacoes', 'obsnota']


class ContratoDelete(DeleteView):
    model = Contrato
    success_url = reverse_lazy('list_contratos')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class QuadroEquipamentoCreate(CreateView):
    model = QuadroEquipamentos
    form_class = QuadroEquipamentoForm

    def get_form_kwargs(self):
        kwargs = super(QuadroEquipamentoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.contrato_id = self.kwargs['contrato_id']
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        quadro = form.save(commit=False)
        quadro.empresa = self.request.user.usuario.empresa
        quadro.save()
        return super(QuadroEquipamentoCreate, self).form_valid(form)


class QuadroEquipamentoEdit(UpdateView):
    model = QuadroEquipamentos
    fields = ['quantidade']


class QuadroEquipamentoDelete(DeleteView):
    model = QuadroEquipamentos
    success_url = reverse_lazy('list_contratos')


class QuadroAcessorioCreate(CreateView):
    model = QuadroAcessorio
    form_class = QuadroAcessorioForm

    def get_form_kwargs(self):
        kwargs = super(QuadroAcessorioCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.contrato_id = self.kwargs['contrato_id']
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        quadro = form.save(commit=False)
        quadro.empresa = self.request.user.usuario.empresa
        quadro.save()
        return super(QuadroAcessorioCreate, self).form_valid(form)


class QuadroAcessorioEdit(UpdateView):
    model = QuadroAcessorio
    fields = ['quantidade']


class QuadroAcessorioDelete(DeleteView):
    model = QuadroAcessorio
    success_url = reverse_lazy('list_contratos')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())

