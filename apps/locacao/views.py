from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import QuadroEquipamentoForm, ContratoForm, QuadroAcessorioForm, ListaEquipamentoForm
from .models import Contrato, QuadroEquipamentos, QuadroAcessorio, ListaEquipamento
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)

from ..empresa.models import Empresa
from ..inventario.models import Equipamento, HistoricoEquipamento


def vincularEquipamento(request, gContrato, gEmpresa):
    request.session['contrato'] = gContrato
    qsCont = Contrato.objects.filter(codigo=gContrato)
    request.session['n_contrato'] = qsCont[0].cliente.nome
    cadastrados = 0
    vinculados = 0
    urlms = '/locacao/vincular_equipamento/' + str(gContrato) + '/' + str(gEmpresa) + '/'
    if qsCont.exists():
        qsQEquip = qsCont[0].quadroequipamentos_set.all()
        if qsQEquip.exists():
            for item in qsQEquip.all():
                quant = item.quantidade
                cadastrados = cadastrados + quant
        qsEquip = qsCont[0].listaequipamento_set.all()
        if qsEquip.exists():
            for item in qsEquip.all():
                vinculados = vinculados + 1
    else:
        messages.warning(request, 'Contrato não foi localizado!')
        return redirect(urlms)
    request.session['cadastrados'] = cadastrados
    request.session['vinculados'] = vinculados
    return render(request, 'locacao/vinculaequipamento_form.html')


def gravaEquipamentoVinculado(request, gContrato, gEmpresa):
    serial = request.POST.get('vincularEquipFormSerie') or ""
    equip = Equipamento.objects.filter(serial=serial)
    lEmpresa = Empresa.objects.filter(pk=gEmpresa)
    empresa_logada = lEmpresa.first()
    lCont = Contrato.objects.filter(codigo=gContrato, empresa=empresa_logada.pk)
    contrato = lCont.first()
    urlms = '/locacao/vincular_equipamento/' + str(gContrato) + '/' + str(gEmpresa) + '/'
    lEqpContrato = contrato.listaequipamento_set.all()
    print(lEqpContrato.all())
    for item in lEqpContrato.all():
        if item.equipamento.serial == serial:
            messages.warning(request, 'O equipamento (' + serial + ') já foi vinculado!')
            return redirect(urlms)
    if not equip:
        messages.warning(request, 'O equipamento (' + serial + ') não foi localizado!')
        return redirect(urlms)
    iEquip = equip.first()
    print(iEquip)
    if not iEquip.ativo:
        messages.warning(request, 'O equipamento (' + serial + ') não foi localizado!')
        return redirect(urlms)
    if iEquip.status == '4':
        messages.warning(request, 'O equipamento (' + serial + ') está perdido!')
        return redirect(urlms)
    if iEquip.status == '3':
        messages.warning(request, 'O equipamento (' + serial + ') está em manutenção!')
        return redirect(urlms)
    if iEquip.status == '2':
        messages.warning(request, 'O equipamento (' + serial + ') está locado!')
        return redirect(urlms)
    if iEquip.status == '1':
        print(iEquip.status)
        iEquip.contract_bond()
        hist = HistoricoEquipamento(
            empresa=empresa_logada,
            descricao='Vinculado ao contrato ' + str(gContrato) + ' empresa ' + str(gEmpresa),
            equipamento=iEquip,
            status='2',
            data_evento=timezone.now()
        )
        hist.save()
        lista = ListaEquipamento(
            empresa=empresa_logada,
            contrato=contrato,
            equipamento=iEquip,
            data_inclusao=timezone.now()
        )
        lista.save()
        messages.success(request, 'O equipamento (' + serial + ') foi vinculado!')
        return redirect(urlms)
    return redirect(urlms)


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


class ListaEquipamentoCreate(CreateView):
    model = ListaEquipamento
    form_class = ListaEquipamentoForm

    def get_form_kwargs(self):
        kwargs = super(ListaEquipamentoCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        print('get_success_url')
        return reverse_lazy('create_lista', args=[self.object.contrato.pk])

    def form_valid(self, form):
        lista = form.save(commit=False)
        lista.empresa = self.request.user.usuario.empresa
        lista.data_inclusao = timezone.now()
        lista.save()
        return super(ListaEquipamentoCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.contrato_id = self.kwargs['contrato_id']
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
