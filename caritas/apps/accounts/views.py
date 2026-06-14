from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (CoordenadorBazarCreateForm, CoordenadorCreateForm, TrocarSenhaForm,
                    UsuarioEditForm, VoluntarioBazarCreateForm, VoluntarioCreateForm)
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .decorators import admin_required, coordenador_bazar_required, coordenador_required
from .models import Usuario


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


# ── Administrador: gerencia coordenadores ─────────────────────────────────────

@login_required
@admin_required
def gerenciar_coordenadores(request):
    coordenadores = Usuario.objects.filter(perfil='coordenador').order_by('paroquia', 'username')
    return render(request, 'accounts/usuarios/coordenadores.html', {'usuarios': coordenadores})


@login_required
@admin_required
def criar_coordenador(request):
    if request.method == 'POST':
        form = CoordenadorCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coordenador criado com sucesso!')
            return redirect('accounts:gerenciar_coordenadores')
    else:
        form = CoordenadorCreateForm()
    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': 'Novo Coordenador',
        'cancelar_url': 'accounts:gerenciar_coordenadores',
    })


# ── Administrador: gerencia coordenadores do bazar ───────────────────────────

@login_required
@admin_required
def criar_coordenador_bazar(request):
    if request.method == 'POST':
        form = CoordenadorBazarCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coordenador do Bazar criado com sucesso!')
            return redirect('accounts:gerenciar_coordenadores')
    else:
        form = CoordenadorBazarCreateForm()
    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': 'Novo Coordenador do Bazar',
        'cancelar_url': 'accounts:gerenciar_coordenadores',
    })


# ── Coordenador do Bazar: gerencia voluntários do bazar ──────────────────────

@login_required
@coordenador_bazar_required
def gerenciar_voluntarios_bazar(request):
    voluntarios = Usuario.objects.filter(perfil='voluntario_bazar')
    return render(request, 'accounts/usuarios/voluntarios_bazar.html', {'usuarios': voluntarios})


@login_required
@coordenador_bazar_required
def criar_voluntario_bazar(request):
    if request.method == 'POST':
        form = VoluntarioBazarCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voluntário do Bazar criado com sucesso!')
            return redirect('accounts:gerenciar_voluntarios_bazar')
    else:
        form = VoluntarioBazarCreateForm()
    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': 'Novo Voluntário do Bazar',
        'cancelar_url': 'accounts:gerenciar_voluntarios_bazar',
    })


# ── Coordenador: gerencia voluntários da sua paróquia ─────────────────────────

@login_required
@coordenador_required
def gerenciar_voluntarios(request):
    if request.user.perfil == 'administrador':
        voluntarios = Usuario.objects.filter(perfil='voluntario').order_by('paroquia', 'username')
    else:
        voluntarios = Usuario.objects.filter(perfil='voluntario', paroquia=request.user.paroquia)
    return render(request, 'accounts/usuarios/voluntarios.html', {'usuarios': voluntarios})


@login_required
@coordenador_required
def criar_voluntario(request):
    if request.method == 'POST':
        form = VoluntarioCreateForm(request.POST)
        if form.is_valid():
            voluntario = form.save(commit=False)
            voluntario.paroquia = request.user.paroquia
            voluntario.save()
            messages.success(request, f'Voluntário {voluntario.username} criado com sucesso!')
            return redirect('accounts:gerenciar_voluntarios')
    else:
        form = VoluntarioCreateForm()
    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': 'Novo Voluntário',
        'cancelar_url': 'accounts:gerenciar_voluntarios',
    })


# ── Compartilhado: editar, toggle e trocar senha ──────────────────────────────

@login_required
@coordenador_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.user.perfil == 'coordenador' and usuario.paroquia != request.user.paroquia:
        raise PermissionDenied
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario.username} atualizado!')
            voltar = 'accounts:gerenciar_coordenadores' if usuario.perfil == 'coordenador' else 'accounts:gerenciar_voluntarios'
            return redirect(voltar)
    else:
        form = UsuarioEditForm(instance=usuario)
    cancelar = 'accounts:gerenciar_coordenadores' if usuario.perfil == 'coordenador' else 'accounts:gerenciar_voluntarios'
    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': f'Editar {usuario.username}',
        'cancelar_url': cancelar,
    })


@login_required
@coordenador_required
def toggle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.user.perfil == 'coordenador' and usuario.paroquia != request.user.paroquia:
        raise PermissionDenied
    usuario.is_active = not usuario.is_active
    usuario.save()
    status = 'ativado' if usuario.is_active else 'desativado'
    messages.success(request, f'Usuário {usuario.username} {status}.')
    voltar = 'accounts:gerenciar_coordenadores' if usuario.perfil == 'coordenador' else 'accounts:gerenciar_voluntarios'
    return redirect(voltar)


@login_required
@coordenador_required
def trocar_senha(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.user.perfil == 'coordenador':
        if usuario.perfil != 'voluntario' or usuario.paroquia != request.user.paroquia:
            raise PermissionDenied
    if request.method == 'POST':
        form = TrocarSenhaForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Senha de {usuario.username} alterada com sucesso!')
            voltar = 'accounts:gerenciar_coordenadores' if usuario.perfil == 'coordenador' else 'accounts:gerenciar_voluntarios'
            return redirect(voltar)
    else:
        form = TrocarSenhaForm(usuario)
    return render(request, 'accounts/usuarios/trocar_senha.html', {
        'form': form,
        'usuario': usuario,
    })
