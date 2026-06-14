from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Count
from django.utils import timezone
from apps.accounts.decorators import bazar_required, coordenador_bazar_required
from .models import ItemEstoqueBazar, EntradaBazar, ItemEntradaBazar, Venda, EmpresaParceira
from .forms import (EntradaBazarForm, ItemEntradaBazarFormSet, VendaForm,
                    ItemEstoqueBazarForm, EmpresaParceiraForm)


@login_required
@bazar_required
def dashboard(request):
    hoje = timezone.now().date()
    contexto = {
        'total_itens': ItemEstoqueBazar.objects.aggregate(total=Sum('quantidade'))['total'] or 0,
        'total_vendas_mes': Venda.objects.filter(data__month=hoje.month, data__year=hoje.year).aggregate(total=Sum('valor_total'))['total'] or 0,
        'total_doacoes_mes': EntradaBazar.objects.filter(data__month=hoje.month, data__year=hoje.year).count(),
        'receita_financeira_mes': EntradaBazar.objects.filter(
            tipo_entrada='doacao_financeira',
            data__month=hoje.month,
            data__year=hoje.year
        ).aggregate(total=Sum('valor'))['total'] or 0,
    }
    return render(request, 'bazar/dashboard.html', contexto)


# ── Estoque ────────────────────────────────────────────────────────────────────

@login_required
@bazar_required
def estoque_listagem(request):
    itens = ItemEstoqueBazar.objects.all()
    return render(request, 'bazar/estoque/listagem.html', {'itens': itens})


@login_required
@coordenador_bazar_required
def estoque_adicionar(request):
    if request.method == 'POST':
        form = ItemEstoqueBazarForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.registrado_por = request.user
            item.save()
            messages.success(request, 'Item adicionado ao estoque do bazar!')
            return redirect('bazar:estoque_listagem')
    else:
        form = ItemEstoqueBazarForm()
    return render(request, 'bazar/estoque/adicionar.html', {'form': form})


# ── Doações / Entradas ─────────────────────────────────────────────────────────

@login_required
@bazar_required
def doacoes_listagem(request):
    entradas = EntradaBazar.objects.select_related('empresa', 'registrado_por').all()
    return render(request, 'bazar/doacoes/listagem.html', {'entradas': entradas})


@login_required
@bazar_required
def doacoes_registrar(request):
    if request.method == 'POST':
        form = EntradaBazarForm(request.POST)
        formset = ItemEntradaBazarFormSet(request.POST)
        tipo_entrada = request.POST.get('tipo_entrada')
        if form.is_valid():
            if tipo_entrada == 'doacao_financeira' or formset.is_valid():
                try:
                    with transaction.atomic():
                        entrada = form.save(commit=False)
                        entrada.registrado_por = request.user
                        entrada.save()
                        if tipo_entrada == 'doacao_item':
                            itens = formset.save(commit=False)
                            for item in itens:
                                item.entrada = entrada
                                item.save()
                                ItemEstoqueBazar.objects.create(
                                    descricao=item.descricao,
                                    categoria=item.categoria,
                                    tamanho=item.tamanho,
                                    estado=item.estado,
                                    quantidade=item.quantidade,
                                    preco_sugerido=item.preco_sugerido,
                                    registrado_por=request.user,
                                )
                        messages.success(request, 'Entrada registrada com sucesso!')
                        return redirect('bazar:doacoes_listagem')
                except Exception as e:
                    messages.error(request, f'Erro ao registrar entrada: {str(e)}')
    else:
        form = EntradaBazarForm()
        formset = ItemEntradaBazarFormSet()
    return render(request, 'bazar/doacoes/registrar.html', {'form': form, 'formset': formset})


# ── Vendas ─────────────────────────────────────────────────────────────────────

@login_required
@bazar_required
def vendas_listagem(request):
    vendas = Venda.objects.select_related('item', 'registrado_por').all()
    total_geral = vendas.aggregate(total=Sum('valor_total'))['total'] or 0
    return render(request, 'bazar/vendas/listagem.html', {'vendas': vendas, 'total_geral': total_geral})


@login_required
@bazar_required
def vendas_registrar(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    venda = form.save(commit=False)
                    venda.registrado_por = request.user
                    item = venda.item
                    if item.quantidade < venda.quantidade:
                        messages.error(request, f'Estoque insuficiente. Disponível: {item.quantidade}.')
                        return render(request, 'bazar/vendas/registrar.html', {'form': form})
                    item.quantidade -= venda.quantidade
                    item.save()
                    venda.save()
                    messages.success(request, 'Venda registrada e estoque atualizado!')
                    return redirect('bazar:vendas_listagem')
            except Exception as e:
                messages.error(request, f'Erro ao registrar venda: {str(e)}')
    else:
        form = VendaForm()
    return render(request, 'bazar/vendas/registrar.html', {'form': form})


# ── Empresas Parceiras ─────────────────────────────────────────────────────────

@login_required
@coordenador_bazar_required
def empresas_listagem(request):
    empresas = EmpresaParceira.objects.all()
    return render(request, 'bazar/empresas/listagem.html', {'empresas': empresas})


@login_required
@coordenador_bazar_required
def empresas_form(request, pk=None):
    empresa = get_object_or_404(EmpresaParceira, pk=pk) if pk else None
    if request.method == 'POST':
        form = EmpresaParceiraForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa salva com sucesso!')
            return redirect('bazar:empresas_listagem')
    else:
        form = EmpresaParceiraForm(instance=empresa)
    return render(request, 'bazar/empresas/form.html', {
        'form': form,
        'titulo': 'Editar Empresa' if empresa else 'Nova Empresa Parceira',
    })


# ── Relatório do Bazar ─────────────────────────────────────────────────────────

@login_required
@coordenador_bazar_required
def relatorio(request):
    hoje = timezone.now().date()
    mes, ano = hoje.month, hoje.year

    vendas_mes = Venda.objects.filter(data__month=mes, data__year=ano)
    entradas_mes = EntradaBazar.objects.filter(data__month=mes, data__year=ano)

    contexto = {
        'receita_vendas': vendas_mes.aggregate(total=Sum('valor_total'))['total'] or 0,
        'qtd_vendas': vendas_mes.count(),
        'receita_financeira': entradas_mes.filter(tipo_entrada='doacao_financeira').aggregate(total=Sum('valor'))['total'] or 0,
        'qtd_doacoes_item': entradas_mes.filter(tipo_entrada='doacao_item').count(),
        'itens_mais_vendidos': ItemEstoqueBazar.objects.annotate(
            total_vendido=Sum('vendas__quantidade')
        ).order_by('-total_vendido')[:5],
        'vendas_mes': vendas_mes.select_related('item'),
        'mes_atual': hoje.strftime('%B de %Y'),
    }
    return render(request, 'bazar/relatorios/index.html', contexto)
