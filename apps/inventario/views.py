from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import EquipamentoForm, EquipamentoPerdidoForm
from .models import TipoEquipamento, Equipamento, Acessorio, HistoricoEquipamento, EquipamentoPerdido
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)

from ..locacao.models import ListaEquipamento, Contrato


class EquipamentoPerdidoCreate(CreateView):
    model = EquipamentoPerdido
    form_class = EquipamentoPerdidoForm

    def get_context_data(self, **kwargs):
        context = super(EquipamentoPerdidoCreate, self).get_context_data(**kwargs)
        context['hist'] = HistoricoEquipamento.objects.filter(equipamento=self.kwargs['equipamento_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super(EquipamentoPerdidoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.equipamento_id = self.kwargs['equipamento_id']
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        print('get_success_url')
        return reverse_lazy('edit_equipamentos', args=[self.object.equipamento.pk])

    def form_valid(self, form):
        perda = form.save(commit=False)
        perda.empresa = self.request.user.usuario.empresa
        perda.data_evento = timezone.now()
        equipamento = Equipamento.objects.get(serial=self.kwargs['equipamento_id'])
        lista_eqp = equipamento.listaequipamento_set.last()
        contrato = Contrato.objects.get(codigo=lista_eqp.contrato.pk)
        equipamento.set_lost()
        equipamento.save()
        perda.ultimo_contrato = contrato.pk
        perda.save()
        hist = HistoricoEquipamento(
            empresa=self.request.user.usuario.empresa,
            descricao='Equipamento informado como PERDIDO/ROUBADO!',
            usuario=self.request.user.usuario,
            equipamento=equipamento,
            status=equipamento.status,
            data_evento=timezone.now()
        )
        hist.save()
        return super(EquipamentoPerdidoCreate, self).form_valid(form)


class EquipamentoPerdidoEdit(UpdateView):
    model = EquipamentoPerdido
    form_class = EquipamentoPerdidoForm

    def get_form_kwargs(self):
        kwargs = super(EquipamentoPerdidoEdit, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('edit_equipamentos', args=[self.object.equipamento.pk])

    def form_valid(self, form):
        perda = form.save(commit=False)
        contrato = Contrato.objects.get(codigo=self.object.ultimo_contrato)
        equipamento = self.object.equipamento
        for item in contrato.listaequipamento_set.all():
            if item.equipamento == equipamento:
                item.soft_delete()
        equipamento.status = '1'
        equipamento.save()
        perda.soft_delete()
        perda.save()
        hist = HistoricoEquipamento(
            empresa=self.request.user.usuario.empresa,
            descricao='Equipamento informado como RECUPERADO!',
            usuario=self.request.user.usuario,
            equipamento=equipamento,
            status=equipamento.status,
            data_evento=timezone.now()
        )
        hist.save()
        return super(EquipamentoPerdidoEdit, self).form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super(EquipamentoEdit, self).get_context_data(**kwargs)
        qs = EquipamentoPerdido.objects.filter(equipamento=self.object.serial)
        reg_perda = qs.last()
        context['perda'] = reg_perda
        ultimo_contrato = Contrato.objects.get(codigo=reg_perda.ultimo_contrato)
        context['ultimo_contrato'] = ultimo_contrato
        return context


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
            empresa=self.request.user.usuario.empresa,
            descricao='Equipamento incluído!',
            usuario=self.request.user.usuario,
            equipamento=equipamento,
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
        hist = HistoricoEquipamento(
            empresa=self.object.empresa,
            descricao='Equipamento excluído!',
            usuario=self.request.user.usuario,
            equipamento=self.object,
            status=self.object.status,
            data_evento=timezone.now()
        )
        hist.save()
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
