from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import *
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)


class UsuariosList(ListView):
    model = Usuario

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return Usuario.objects.filter(empresa=empresa_in)


class UsuariosEdit(UpdateView):
    model = Usuario
    fields = ['nome', 'sobrenome', 'email', 'telefone', 'cargo', 'observacao']


class UsuariosCreate(CreateView):
    model = Usuario
    fields = ['nome', 'sobrenome', 'email', 'telefone', 'cargo', 'observacao']

    def form_valid(self, form):
        usuario = form.save(commit=False)
        user = User.objects.create(
            username=usuario.email,
            first_name=usuario.nome,
            last_name=usuario.sobrenome)
        user.set_password(usuario.sobrenome)
        user.save()
        usuario.empresa = self.request.user.usuario.empresa
        usuario.user = user
        usuario.save()
        return super(UsuariosCreate, self).form_valid(form)


class ClientesList(ListView):
    model = Cliente

    def get_queryset(self):
        empresa_in = self.request.user.usuario.empresa
        return Cliente.objects.filter(empresa=empresa_in, ativo=True)


class ClientesEdit(UpdateView):
    model = Cliente
    fields = ['nome', 'razaoSocial', 'responsavel', 'inscestadual', 'inscmunicipal',
              'telefone', 'email', 'site', 'endRua', 'endComplemento', 'endCidade', 'endUF',
              'endCEP', 'senhaWeb', 'tipo', 'restricao', 'textorestricao']


class ClientesCreate(CreateView):
    model = Cliente
    fields = ['cnpjCpf', 'nome', 'razaoSocial', 'responsavel', 'inscestadual', 'inscmunicipal',
              'telefone', 'email', 'site', 'endRua', 'endComplemento', 'endCidade', 'endUF',
              'endCEP', 'senhaWeb', 'tipo']

    def form_valid(self, form):
        cliente = form.save(commit=False)
        cliente.empresa = self.request.user.usuario.empresa
        cliente.save()
        return super(ClientesCreate, self).form_valid(form)

class ClientesDelete(DeleteView):
    model = Cliente
    success_url = reverse_lazy('list_clientes')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
