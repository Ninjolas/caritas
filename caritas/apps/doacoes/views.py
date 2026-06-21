from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import coordenador_required
from apps.estoque.models import ItemEstoque

from .forms import DoacaoForm, ItemDoacaoFormSet, get_produtos_json
from .models import Doacao, ItemDoacao


@login_required
def listagem(request):
    is_admin = request.user.perfil == 'administrador'
    paroquia_usuario = request.user.paroquia
    if is_admin:
        doacoes = Doacao.objects.all().order_by('-data')
    else:
        doacoes = Doacao.objects.filter(paroquia=paroquia_usuario).order_by('-data')
    return render(request, 'doacoes/listagem.html', {
        'doacoes': doacoes,
        'is_admin': is_admin,
        'paroquia_usuario': paroquia_usuario,
    })


@login_required
def registrar(request):
    paroquia = request.user.paroquia
    form_kwargs = {'paroquia': paroquia}
    if request.method == 'POST':
        form = DoacaoForm(request.POST)
        formset = ItemDoacaoFormSet(request.POST, form_kwargs=form_kwargs)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    doacao = form.save(commit=False)
                    doacao.paroquia = paroquia
                    doacao.registrado_por = request.user
                    doacao.save()
                    itens = formset.save(commit=False)
                    for item in itens:
                        item.doacao = doacao
                        item.save()
                        ItemEstoque.objects.create(
                            paroquia=doacao.paroquia,
                            produto=item.produto,
                            nome=item.nome,
                            categoria=item.categoria,
                            quantidade=item.quantidade,
                            unidade=item.unidade,
                            validade=item.data_validade,
                            registrado_por=request.user,
                        )
                    messages.success(request, 'Doação registrada e estoque atualizado com sucesso!')
                    return redirect('doacoes:listagem')
            except Exception as e:
                messages.error(request, f'Erro ao registrar doação: {str(e)}')
    else:
        form = DoacaoForm()
        formset = ItemDoacaoFormSet(form_kwargs=form_kwargs)
    return render(request, 'doacoes/registrar.html', {
        'form': form,
        'formset': formset,
        'produtos_json': get_produtos_json(paroquia),
    })


@login_required
@coordenador_required
def editar_doacao(request, pk):
    doacao = get_object_or_404(Doacao, pk=pk)
    if request.user.perfil != 'administrador' and doacao.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        form = DoacaoForm(request.POST, instance=doacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doação atualizada com sucesso!')
            return redirect('doacoes:listagem')
    else:
        form = DoacaoForm(instance=doacao)
    return render(request, 'doacoes/editar_doacao.html', {'form': form, 'doacao': doacao})


@login_required
@coordenador_required
def remover_doacao(request, pk):
    doacao = get_object_or_404(Doacao, pk=pk)
    if request.user.perfil != 'administrador' and doacao.paroquia != request.user.paroquia:
        raise PermissionDenied

    if request.method == 'POST':
        doacao.delete()
        messages.success(request, 'Doação removida com sucesso.')
    return redirect('doacoes:listagem')
