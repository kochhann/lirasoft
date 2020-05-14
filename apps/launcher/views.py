from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.empresa.models import *
from apps.launcher.forms import SignUpForm


@login_required
def home(request):
    return render(request, 'launcher/index.html')


@login_required
def dashboard(request):
    request.session['empresa'] = request.user.usuario.empresa.nome
    return render(request, 'launcher/dashboard.html')


def cadastrar_usuario(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        return redirect('home')
    return render(request, 'empresa/cadastro.html', {'form': form})
