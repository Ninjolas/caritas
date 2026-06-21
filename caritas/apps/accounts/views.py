from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .decorators import admin_required, coordenador_required
from .forms import ParoquiaForm, TrocarSenhaForm, UsuarioCreateForm, UsuarioEditForm
from .models import Paroquia, Usuario


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


# ── Usuários: gerenciamento unificado ────────────────────────────────────────

@login_required
def gerenciar_usuarios(request):
    perfil = request.user.perfil
    if perfil == 'administrador':
        usuarios = Usuario.objects.exclude(perfil='administrador').order_by('paroquia__nome', 'perfil', 'username')
    elif perfil == 'coordenador':
        usuarios = Usuario.objects.filter(
            perfil='voluntario', paroquia=request.user.paroquia
        ).order_by('username')
    elif perfil == 'coordenador_bazar':
        usuarios = Usuario.objects.filter(perfil='voluntario_bazar').order_by('username')
    else:
        raise PermissionDenied
    return render(request, 'accounts/usuarios/listagem.html', {'usuarios': usuarios})


@login_required
def criar_usuario(request):
    perfil = request.user.perfil
    if perfil not in ['administrador', 'coordenador', 'coordenador_bazar']:
        raise PermissionDenied

    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, solicitante=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            if perfil == 'coordenador':
                usuario.perfil = 'voluntario'
                usuario.paroquia = request.user.paroquia
            elif perfil == 'coordenador_bazar':
                usuario.perfil = 'voluntario_bazar'
                usuario.paroquia = None
            usuario.save()
            messages.success(request, f'Usuário {usuario.username} criado com sucesso!')
            return redirect('accounts:gerenciar_usuarios')
    else:
        form = UsuarioCreateForm(solicitante=request.user)

    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': 'Novo Usuário',
        'cancelar_url': 'accounts:gerenciar_usuarios',
    })


@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    perfil_solicitante = request.user.perfil

    if perfil_solicitante not in ['administrador', 'coordenador', 'coordenador_bazar']:
        raise PermissionDenied
    if perfil_solicitante == 'coordenador' and usuario.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario, solicitante=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario.username} atualizado!')
            return redirect('accounts:gerenciar_usuarios')
    else:
        form = UsuarioEditForm(instance=usuario, solicitante=request.user)

    return render(request, 'accounts/usuarios/form.html', {
        'form': form,
        'titulo': f'Editar {usuario.username}',
        'cancelar_url': 'accounts:gerenciar_usuarios',
    })


@login_required
def toggle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    perfil = request.user.perfil
    if perfil not in ['administrador', 'coordenador', 'coordenador_bazar']:
        raise PermissionDenied
    if perfil == 'coordenador' and usuario.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        usuario.is_active = not usuario.is_active
        usuario.save()
        status = 'ativado' if usuario.is_active else 'desativado'
        messages.success(request, f'Usuário {usuario.username} {status}.')
    return redirect('accounts:gerenciar_usuarios')


@login_required
def trocar_senha(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    perfil = request.user.perfil
    if perfil == 'coordenador':
        if usuario.perfil != 'voluntario' or usuario.paroquia != request.user.paroquia:
            raise PermissionDenied
    elif perfil not in ['administrador', 'coordenador_bazar']:
        raise PermissionDenied

    if request.method == 'POST':
        form = TrocarSenhaForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Senha de {usuario.username} alterada com sucesso!')
            return redirect('accounts:gerenciar_usuarios')
    else:
        form = TrocarSenhaForm(usuario)

    return render(request, 'accounts/usuarios/trocar_senha.html', {
        'form': form,
        'usuario': usuario,
    })


# ── Paróquias ─────────────────────────────────────────────────────────────────

@login_required
@admin_required
def gerenciar_paroquias(request):
    paroquias = Paroquia.objects.all()
    return render(request, 'accounts/paroquias/listagem.html', {'paroquias': paroquias})


@login_required
@admin_required
def criar_paroquia(request):
    if request.method == 'POST':
        form = ParoquiaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paróquia criada com sucesso!')
            return redirect('accounts:gerenciar_paroquias')
    else:
        form = ParoquiaForm()
    return render(request, 'accounts/paroquias/form.html', {
        'form': form, 'titulo': 'Nova Paróquia',
    })


@login_required
@admin_required
def editar_paroquia(request, pk):
    paroquia = get_object_or_404(Paroquia, pk=pk)
    if request.method == 'POST':
        form = ParoquiaForm(request.POST, instance=paroquia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paróquia atualizada!')
            return redirect('accounts:gerenciar_paroquias')
    else:
        form = ParoquiaForm(instance=paroquia)
    return render(request, 'accounts/paroquias/form.html', {
        'form': form, 'titulo': f'Editar {paroquia.nome}',
    })


@login_required
@admin_required
def remover_paroquia(request, pk):
    paroquia = get_object_or_404(Paroquia, pk=pk)
    if request.method == 'POST':
        try:
            paroquia.delete()
            messages.success(request, 'Paróquia removida com sucesso. Dados vinculados foram removidos em cascata.')
        except Exception:
            messages.error(request, 'Não é possível remover esta paróquia pois ela possui vendas ou cestas montadas vinculadas. Remova esses registros antes.')
    return redirect('accounts:gerenciar_paroquias')


# ── Compatibilidade: redirects para URLs antigas referenciadas nos templates ──

@login_required
def gerenciar_voluntarios(request):
    return redirect('accounts:gerenciar_usuarios')


@login_required
def gerenciar_coordenadores(request):
    return redirect('accounts:gerenciar_usuarios')


@login_required
def gerenciar_voluntarios_bazar(request):
    return redirect('accounts:gerenciar_usuarios')
