from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import EquipamentoForm
from .models import TipoEquipamento, Equipamento, Acessorio, HistoricoEquipamento
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)

from ..empresa.models import Empresa


class TipoEquipamentoList(ListView):
    model = TipoEquipamento

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return TipoEquipamento.objects.filter(empresa=empresa_in, ativo=True)


class TipoEquipamentoEdit(UpdateView):
    model = TipoEquipamento
    fields = ['marca', 'modelo', 'preco']


class TipoEquipamentoCreate(CreateView):
    model = TipoEquipamento
    fields = ['marca', 'modelo', 'preco']

    def form_valid(self, form):
        tipo_eq = form.save(commit=False)
        tipo_eq.empresa = self.request.user.usuario.empresa
        tipo_eq.save()
        return super(TipoEquipamentoCreate, self).form_valid(form)


class TipoEquipamentoDelete(DeleteView):
    model = TipoEquipamento
    success_url = reverse_lazy('list_tipo_equip')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class EquipamentoList(ListView):
    model = Equipamento

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return Equipamento.objects.filter(empresa=empresa_in, ativo=True)


class EquipamentoEdit(UpdateView):
    model = Equipamento
    fields = ['tipo', 'status']


class EquipamentoCreate(CreateView):
    model = Equipamento
    form_class = EquipamentoForm

    def get_form_kwargs(self):
        kwargs = super(EquipamentoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        equipamento = form.save(commit=False)
        equipamento.empresa = self.request.user.usuario.empresa
        equipamento.save()
        hist = HistoricoEquipamento(
            empresa=self.request.user.usuario.empresa.pk,
            descricao='Equipamento incluído!',
            equipamento=equipamento.serial,
            status='1',
            data_evento=timezone.now()
        )
        hist.save()
        return super(EquipamentoCreate, self).form_valid(form)


class EquipamentoDelete(DeleteView):
    model = Equipamento
    success_url = reverse_lazy('list_equipamentos')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class AcessorioList(ListView):
    model = Acessorio

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return Acessorio.objects.filter(empresa=empresa_in, ativo=True)


class AcessorioEdit(UpdateView):
    model = Acessorio
    fields = ['descricao', 'preco', 'quantidade']


class AcessorioCreate(CreateView):
    model = Acessorio
    fields = ['descricao', 'preco', 'quantidade']

    def form_valid(self, form):
        acessorio = form.save(commit=False)
        acessorio.empresa = self.request.user.usuario.empresa
        acessorio.save()
        return super(AcessorioCreate, self).form_valid(form)


class AcessorioDelete(DeleteView):
    model = Acessorio
    success_url = reverse_lazy('list_acessorios')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
