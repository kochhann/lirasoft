from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import *
from .models import Contrato, QuadroEquipamentos, QuadroAcessorio, ListaEquipamento
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)

from ..empresa.models import Empresa
from ..inventario.models import Equipamento, HistoricoEquipamento, Acessorio


def vincularEquipamento(request, gContrato):
    request.session['contrato'] = gContrato
    empresa = request.user.usuario.empresa.pk
    qsCont = Contrato.objects.filter(codigo=gContrato, ativo=True, empresa=empresa)
    request.session['n_contrato'] = qsCont[0].cliente.nome
    cadastrados = 0
    vinculados = 0
    urlms = '/locacao/vincular_equipamento/' + str(gContrato) + '/'
    if qsCont.exists():
        qsQEquip = qsCont[0].quadroequipamentos_set.all()
        if qsQEquip.exists():
            for item in qsQEquip.all():
                quant = item.quantidade
                cadastrados = cadastrados + quant
        qsEquip = qsCont[0].listaequipamento_set.all()
        if qsEquip.exists():
            for item in qsEquip.all():
                if item.ativo:
                    vinculados = vinculados + 1
    else:
        messages.warning(request, 'Contrato não foi localizado!')
        return redirect(urlms)
    request.session['cadastrados'] = cadastrados
    request.session['vinculados'] = vinculados
    return render(request, 'locacao/vinculaequipamento_form.html')


def gravaEquipamentoVinculado(request, gContrato):
    urlms = '/locacao/vincular_equipamento/' + str(gContrato) + '/'
    serial = request.POST.get('vincularEquipFormSerie') or ""
    empresa = request.user.usuario.empresa
    try:
        equip = Equipamento.objects.get(serial=serial, empresa=empresa.pk)
    except:
        messages.warning(request, 'O equipamento (' + serial + ') não foi localizado!')
        return redirect(urlms)
    if not equip.ativo:
        messages.warning(request, 'O equipamento (' + serial + ') foi excluído em ' + equip.data_desativado.strftime('%d/%m/%Y') + '!')
        return redirect(urlms)
    contrato = Contrato.objects.get(codigo=gContrato, empresa=empresa.pk)
    lEqpContrato = contrato.listaequipamento_set.all()
    print(lEqpContrato.all())
    for item in lEqpContrato.all():
        if item.equipamento.serial == serial and item.ativo:
            messages.warning(request, 'O equipamento (' + serial + ') já foi vinculado!')
            return redirect(urlms)
    if not equip:
        messages.warning(request, 'O equipamento (' + serial + ') não foi localizado!')
        return redirect(urlms)
    if not equip.ativo:
        messages.warning(request, 'O equipamento (' + serial + ') não foi localizado!')
        return redirect(urlms)
    if equip.status == '4':
        messages.warning(request, 'O equipamento (' + serial + ') está perdido!')
        return redirect(urlms)
    if equip.status == '3':
        messages.warning(request, 'O equipamento (' + serial + ') está em manutenção!')
        return redirect(urlms)
    if equip.status == '2':
        messages.warning(request, 'O equipamento (' + serial + ') está locado!')
        return redirect(urlms)
    if equip.status == '1':
        print(equip.status)
        equip.contract_bond()
        hist = HistoricoEquipamento(
            empresa=empresa,
            descricao='Vinculado ao contrato ' + str(gContrato) + ' empresa ' + contrato.cliente.nome,
            usuario=request.user.usuario,
            equipamento=equip,
            status=equip.status,
            data_evento=timezone.now()
        )
        hist.save()
        lista = ListaEquipamento(
            empresa=empresa,
            contrato=contrato,
            equipamento=equip,
            data_inclusao=timezone.now()
        )
        lista.save()
        messages.success(request, 'O equipamento (' + serial + ') foi vinculado!')
        return redirect(urlms)
    return redirect(urlms)


def desvincularEquipamento(request, gContrato):
    request.session['contrato'] = gContrato
    empresa = request.user.usuario.empresa.pk
    contrato = Contrato.objects.get(codigo=gContrato, ativo=True, empresa=empresa)
    request.session['n_contrato'] = contrato.cliente.nome
    vinculados = 0
    urlms = '/locacao/desvincular_equipamento/' + str(gContrato) + '/'
    if contrato:
        qsEquip = contrato.listaequipamento_set.all()
        if qsEquip.exists():
            for item in qsEquip.all():
                if item.ativo:
                    vinculados = vinculados + 1
    else:
        messages.warning(request, 'Contrato não foi localizado!')
        return redirect(urlms)
    request.session['vinculados'] = vinculados
    return render(request, 'locacao/desvinculaequipamento_form.html')


def gravaEquipamentoDesvinculado(request, gContrato):
    serial = request.POST.get('desvincularEquipFormSerie') or ""
    empresa = request.user.usuario.empresa
    urlms = '/locacao/desvincular_equipamento/' + str(gContrato) + '/'
    try:
        equipamento = Equipamento.objects.get(serial=serial, empresa=empresa.pk)
    except:
        messages.warning(request, 'O equipamento (' + serial + ') não foi localizado!')
        return redirect(urlms)
    if not equipamento.ativo:
        messages.warning(request, 'O equipamento (' + serial + ') foi excluído em ' + equipamento.data_desativado.strftime('%d/%m/%Y') + '!')
        return redirect(urlms)

    contrato = Contrato.objects.get(codigo=gContrato, empresa=empresa.pk)
    lEqpContrato = contrato.listaequipamento_set.all()
    contem = False
    for item in lEqpContrato.all():
        if item.equipamento.serial == serial and item.ativo:
            item.soft_delete()
            contem = True
    if contem:
        equipamento.contract_unbond()
        hist = HistoricoEquipamento(
            empresa=empresa,
            descricao='Desvinculado do contrato ' + str(gContrato) + ' empresa ' + contrato.cliente.nome,
            equipamento=equipamento,
            usuario=request.user.usuario,
            status=equipamento.status,
            data_evento=timezone.now()
        )
        hist.save()
        messages.warning(request, 'O equipamento (' + serial + ') foi desvinculado!')
        return redirect(urlms)
    messages.warning(request, 'O equipamento (' + serial + ') não está neste contrato!')
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
        qsEquip = self.object.quadroequipamentos_set.all()
        qsAcess = self.object.quadroacessorio_set.all()
        if qsAcess.exists():
            for item in qsAcess.all():
                item.soft_delete()
        if qsEquip.exists():
            for item in qsEquip.all():
                item.delete()
        lsEquip = self.object.listaequipamento_set.all()
        if lsEquip.exists():
            for item in lsEquip.all():
                if item.ativo:
                    item.soft_delete()
                    e = Equipamento.objects.filter(serial=item.equipamento.pk)
                    eqp = e.first()
                    eqp.contract_unbond()
                    hist = HistoricoEquipamento(
                        empresa=item.empresa.pk,
                        descricao='Desvinculado do contrato ' + str(self.object.pk) +
                                  ' empresa ' + str(self.object.empresa.pk),
                        equipamento=eqp.serial,
                        status='1',
                        data_evento=timezone.now()
                    )
                    hist.save()
        messages.success(request, 'Contrato finalizado!')
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
        a = Acessorio.objects.filter(codigo=quadro.acessorio.pk)
        ac = a.first()
        if ac.quantidade >= quadro.quantidade:
            ac.quantidade = ac.quantidade - quadro.quantidade
            ac.save()
        else:
            return super(QuadroAcessorioCreate, self).form_valid(form)
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
