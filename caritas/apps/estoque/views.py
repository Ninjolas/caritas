from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import coordenador_required, modulo_paroquia_required

from .forms import ItemEstoqueForm, ItemEstoqueEditarForm, ProdutoCatalogoForm
from .models import ItemEstoque, ProdutoCatalogo


@login_required
@modulo_paroquia_required
def listagem(request):
    is_admin = request.user.perfil == 'administrador'
    paroquia_usuario = request.user.paroquia
    if is_admin:
        itens = ItemEstoque.objects.all().order_by('paroquia__nome', 'nome')
    else:
        itens = ItemEstoque.objects.filter(paroquia=paroquia_usuario)
    return render(request, 'estoque/listagem.html', {
        'itens': itens,
        'is_admin': is_admin,
        'paroquia_usuario': paroquia_usuario,
    })


@login_required
@coordenador_required
def entrada(request):
    paroquia = request.user.paroquia
    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST, paroquia=paroquia)
        if form.is_valid():
            item = form.save(commit=False)
            item.paroquia = paroquia
            item.registrado_por = request.user
            item.save()
            messages.success(request, 'Item registrado no estoque com sucesso!')
            return redirect('estoque:listagem')
    else:
        form = ItemEstoqueForm(paroquia=paroquia)
    return render(request, 'estoque/entrada.html', {
        'form': form,
        'produtos_json': form.get_produtos_json(),
    })


@login_required
@coordenador_required
def editar_item(request, pk):
    item = get_object_or_404(ItemEstoque, pk=pk)
    if request.user.perfil != 'administrador' and item.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        form = ItemEstoqueEditarForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('estoque:listagem')
    else:
        form = ItemEstoqueEditarForm(instance=item)
    return render(request, 'estoque/editar_item.html', {'form': form, 'item': item})


@login_required
@coordenador_required
def remover_item(request, pk):
    item = get_object_or_404(ItemEstoque, pk=pk)
    if request.user.perfil != 'administrador' and item.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, 'Item removido do estoque.')
        except Exception:
            messages.error(request, 'Não é possível remover este item pois ele está vinculado a registros existentes (vendas ou atendimentos).')
    return redirect('estoque:listagem')


@login_required
@modulo_paroquia_required
def catalogo_listagem(request):
    is_admin = request.user.perfil == 'administrador'
    if is_admin:
        produtos = ProdutoCatalogo.objects.all()
    else:
        produtos = ProdutoCatalogo.objects.filter(paroquia=request.user.paroquia)
    return render(request, 'estoque/catalogo/listagem.html', {'produtos': produtos, 'is_admin': is_admin})


@login_required
@coordenador_required
def catalogo_form(request, pk=None):
    produto = get_object_or_404(ProdutoCatalogo, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProdutoCatalogoForm(request.POST, instance=produto)
        if form.is_valid():
            novo = form.save(commit=False)
            if not pk:
                novo.paroquia = request.user.paroquia
            novo.save()
            acao = 'atualizado' if pk else 'adicionado ao catálogo'
            messages.success(request, f'Produto {acao} com sucesso!')
            return redirect('estoque:catalogo')
    else:
        form = ProdutoCatalogoForm(instance=produto)
    return render(request, 'estoque/catalogo/form.html', {'form': form, 'produto': produto})


@login_required
@coordenador_required
def catalogo_remover(request, pk):
    produto = get_object_or_404(ProdutoCatalogo, pk=pk)
    if request.user.perfil != 'administrador' and produto.paroquia != request.user.paroquia:
        raise PermissionDenied
    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(request, 'Produto removido do catálogo.')
        except Exception:
            messages.error(request, 'Não é possível remover este produto pois ele está vinculado a registros existentes.')
    return redirect('estoque:catalogo')
