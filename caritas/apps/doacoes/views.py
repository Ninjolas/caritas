from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Doacao, ItemDoacao
from .forms import DoacaoForm, ItemDoacaoFormSet
from apps.estoque.models import ItemEstoque


@login_required
def listagem(request):
    paroquia = request.user.paroquia or 'Paróquia Padrão'
    doacoes = Doacao.objects.filter(paroquia=paroquia)
    return render(request, 'doacoes/listagem.html', {'doacoes': doacoes})


@login_required
def registrar(request):
    if request.method == 'POST':
        form = DoacaoForm(request.POST)
        formset = ItemDoacaoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    doacao = form.save(commit=False)
                    doacao.paroquia = request.user.paroquia or 'Paróquia Padrão'
                    doacao.registrado_por = request.user
                    doacao.save()
                    itens = formset.save(commit=False)
                    for item in itens:
                        item.doacao = doacao
                        item.save()
                        if doacao.tipo == 'entrada':
                            ItemEstoque.objects.create(
                                paroquia=doacao.paroquia,
                                nome=item.nome,
                                categoria=item.categoria,
                                quantidade=item.quantidade,
                                unidade=item.unidade,
                                registrado_por=request.user,
                            )
                    messages.success(request, 'Doação registrada e estoque atualizado com sucesso!')
                    return redirect('doacoes:listagem')
            except Exception as e:
                messages.error(request, f'Erro ao registrar doação: {str(e)}')
    else:
        form = DoacaoForm()
        formset = ItemDoacaoFormSet()
    return render(request, 'doacoes/registrar.html', {'form': form, 'formset': formset})
