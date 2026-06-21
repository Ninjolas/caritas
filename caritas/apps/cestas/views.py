from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from .models import CestaPronta, EntregaCesta
from .forms import MontagemForm, ItemMontagemFormSet, DoacaoCestaForm, EntregaCestaForm


def _estoque_cestas(paroquia):
    entradas = CestaPronta.objects.filter(paroquia=paroquia).aggregate(total=Sum('quantidade'))['total'] or 0
    saidas = EntregaCesta.objects.filter(paroquia=paroquia).aggregate(total=Sum('quantidade'))['total'] or 0
    return entradas - saidas


@login_required
def dashboard(request):
    paroquia = request.user.paroquia
    saldo = _estoque_cestas(paroquia)
    ultimas_entregas = EntregaCesta.objects.filter(paroquia=paroquia).select_related('familia')[:5]
    return render(request, 'cestas/dashboard.html', {
        'saldo_cestas': saldo,
        'ultimas_entregas': ultimas_entregas,
    })


@login_required
def registrar_montagem(request):
    if request.method == 'POST':
        form = MontagemForm(request.POST)
        formset = ItemMontagemFormSet(request.POST, paroquia=request.user.paroquia)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    cesta = form.save(commit=False)
                    cesta.paroquia = request.user.paroquia
                    cesta.origem = 'montagem'
                    cesta.registrado_por = request.user
                    cesta.save()
                    itens = formset.save(commit=False)
                    for item_montagem in itens:
                        item_montagem.cesta_pronta = cesta
                        item_estoque = item_montagem.item_estoque
                        item_montagem.item_nome = item_estoque.nome
                        if item_estoque.quantidade < item_montagem.quantidade_total:
                            raise ValueError(
                                f'Estoque insuficiente para {item_estoque.nome}. Disponível: {item_estoque.quantidade}.'
                            )
                        item_estoque.quantidade -= item_montagem.quantidade_total
                        item_estoque.save()
                        item_montagem.save()
                    messages.success(request, f'{cesta.quantidade} cesta(s) montada(s) e estoque atualizado!')
                    return redirect('cestas:dashboard')
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Erro ao registrar montagem: {str(e)}')
    else:
        form = MontagemForm()
        formset = ItemMontagemFormSet(paroquia=request.user.paroquia)
    return render(request, 'cestas/montagem/form.html', {'form': form, 'formset': formset})


@login_required
def registrar_doacao_cesta(request):
    if request.method == 'POST':
        form = DoacaoCestaForm(request.POST)
        if form.is_valid():
            cesta = form.save(commit=False)
            cesta.paroquia = request.user.paroquia
            cesta.origem = 'doacao'
            cesta.registrado_por = request.user
            cesta.save()
            messages.success(request, f'{cesta.quantidade} cesta(s) recebida(s) como doação!')
            return redirect('cestas:dashboard')
    else:
        form = DoacaoCestaForm()
    return render(request, 'cestas/montagem/form.html', {
        'form': form,
        'formset': None,
        'titulo': 'Registrar doação de cestas',
    })


@login_required
def registrar_entrega(request):
    paroquia = request.user.paroquia
    saldo = _estoque_cestas(paroquia)
    if request.method == 'POST':
        form = EntregaCestaForm(request.POST, paroquia=paroquia)
        if form.is_valid():
            entrega = form.save(commit=False)
            if entrega.quantidade > saldo:
                messages.error(request, f'Cestas insuficientes. Disponível: {saldo}.')
            else:
                entrega.paroquia = paroquia
                entrega.registrado_por = request.user
                entrega.save()
                messages.success(request, 'Entrega registrada com sucesso!')
                return redirect('cestas:dashboard')
    else:
        form = EntregaCestaForm(paroquia=paroquia)
    return render(request, 'cestas/entregas/form.html', {'form': form, 'saldo': saldo})


@login_required
def listagem_entregas(request):
    entregas = EntregaCesta.objects.filter(
        paroquia=request.user.paroquia
    ).select_related('familia', 'registrado_por')
    return render(request, 'cestas/entregas/listagem.html', {'entregas': entregas})
