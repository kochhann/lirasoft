from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from apps.empresa.models import Cliente, Empresa
from apps.faturamento.forms import NotaCobrancaForm
from apps.faturamento.models import NotaCobranca
from apps.locacao.models import Contrato
from django.contrib import messages


def Replace(str1):
    maketrans = str1.maketrans
    final = str1.translate(maketrans(',.', '.,'))
    return final


def geraNotaContrato(request, gContrato, gEmpresa):
    request.session['contrato'] = gContrato
    # request.session['empresa'] = gEmpresa
    contrato = Contrato.objects.get(empresa=gEmpresa, codigo=gContrato)
    cliente = Cliente.objects.get(empresa=gEmpresa, cnpjCpf=contrato.cliente.pk)
    request.session['cnpjcliente'] = cliente.cnpjCpf
    request.session['nomecliente'] = cliente.nome
    request.session['valorcontrato'] = str(contrato.valor)
    return render(request, 'faturamento/geranotacontrato_form.html')


def gravaNotaContrato (request, gContrato, gEmpresa):
    urlms = '/locacao/contrato/editar/' + str(gContrato) + '/'
    datafechamento = request.POST.get('dataFechamentoNForm')
    valor = request.POST.get('valorNForm') or "0"
    pedido = request.POST.get('pedidoNForm') or ""
    obs = request.POST.get('obsNotaNForm') or ""
    empr = Empresa.objects.get(cnpjCpf=gEmpresa)
    cont = Contrato.objects.get(empresa=gEmpresa, codigo=gContrato)
    cli = Cliente.objects.get(empresa=gEmpresa, cnpjCpf=cont.cliente.pk)
    print(valor)
    print(Replace(valor))
    nota = NotaCobranca(
        empresa=empr,
        cnpjcliente=cli,
        contrato=cont,
        datafechamento=datetime.strptime(datafechamento, '%d/%m/%Y'),
        valor=Decimal(Replace(valor.replace('.', ''))),
        pedido=pedido,
        obsnota=obs,
        data_inclusao=timezone.now()
    )
    nota.save()

    messages.success(request, 'Nota gerada com sucesso!')
    return redirect(urlms)


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


class NotaCobrancaList(ListView):
    model = NotaCobranca

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return NotaCobranca.objects.filter(empresa=empresa_in, cancelada=False)


class NotaCobrancaEdit(UpdateView):
    model = NotaCobranca
    fields = ['datafechamento', 'cnpjcliente', 'valor', 'contrato', 'pedido',
              'obsnota']


class NotaCobrancaDelete(DeleteView):
    model = NotaCobranca
    success_url = reverse_lazy('list_nota_cobranca')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
