from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import coordenador_required

from .forms import ItemEstoqueForm
from .models import ItemEstoque


@login_required
def listagem(request):
    is_admin = request.user.perfil == 'administrador'
    paroquia_usuario = request.user.paroquia
    if is_admin:
        itens = ItemEstoque.objects.all().order_by('paroquia', 'nome')
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
    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.paroquia = request.user.paroquia or 'Paróquia Padrão'
            item.registrado_por = request.user
            item.save()
            messages.success(request, 'Item registrado no estoque com sucesso!')
            return redirect('estoque:listagem')
    else:
        form = ItemEstoqueForm()
    return render(request, 'estoque/entrada.html', {'form': form})


@login_required
@coordenador_required
def editar_item(request, pk):
    item = get_object_or_404(ItemEstoque, pk=pk)
    if request.user.perfil != 'administrador' and item.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('estoque:listagem')
    else:
        form = ItemEstoqueForm(instance=item)
    return render(request, 'estoque/editar_item.html', {'form': form, 'item': item})


@login_required
@coordenador_required
def remover_item(request, pk):
    item = get_object_or_404(ItemEstoque, pk=pk)
    if request.user.perfil != 'administrador' and item.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item removido do estoque.')
    return redirect('estoque:listagem')
