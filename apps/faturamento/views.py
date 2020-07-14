from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
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
