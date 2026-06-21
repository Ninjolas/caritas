from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.utils import timezone

MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}
from xhtml2pdf import pisa

import json

from apps.accounts.decorators import bazar_required, coordenador_bazar_required
from .models import CatalogoBazar, ItemEstoqueBazar, EntradaBazar, ItemEntradaBazar, Venda, EmpresaParceira
from .forms import (CatalogoBazarForm, EntradaBazarForm, ItemEntradaBazarFormSet, VendaForm,
                    ItemEstoqueBazarForm, EmpresaParceiraForm)


def _pode_ver_financeiro(user):
    return user.perfil in ['coordenador_bazar', 'administrador']


# ── Dashboard ──────────────────────────────────────────────────────────────────

@login_required
@bazar_required
def dashboard(request):
    hoje = timezone.now().date()
    show_financial = _pode_ver_financeiro(request.user)
    contexto = {
        'total_itens': ItemEstoqueBazar.objects.aggregate(total=Sum('quantidade'))['total'] or 0,
        'total_doacoes_mes': EntradaBazar.objects.filter(data__month=hoje.month, data__year=hoje.year).count(),
        'show_financial': show_financial,
    }
    if show_financial:
        contexto['total_vendas_mes'] = Venda.objects.filter(
            data__month=hoje.month, data__year=hoje.year
        ).aggregate(total=Sum('valor_total'))['total'] or 0
        contexto['receita_financeira_mes'] = EntradaBazar.objects.filter(
            tipo_entrada='doacao_financeira',
            data__month=hoje.month, data__year=hoje.year
        ).aggregate(total=Sum('valor'))['total'] or 0
    return render(request, 'bazar/dashboard.html', contexto)


# ── Catálogo ───────────────────────────────────────────────────────────────────

@login_required
@coordenador_bazar_required
def catalogo_listagem(request):
    catalogo = CatalogoBazar.objects.all()
    return render(request, 'bazar/catalogo/listagem.html', {'catalogo': catalogo})


@login_required
@coordenador_bazar_required
def catalogo_form(request, pk=None):
    item = get_object_or_404(CatalogoBazar, pk=pk) if pk else None
    if request.method == 'POST':
        form = CatalogoBazarForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catálogo salvo com sucesso!')
            return redirect('bazar:catalogo_listagem')
    else:
        form = CatalogoBazarForm(instance=item)
    titulo = f'Editar {item.nome}' if item else 'Novo Item do Catálogo'
    return render(request, 'bazar/catalogo/form.html', {'form': form, 'titulo': titulo})


@login_required
@coordenador_bazar_required
def catalogo_remover(request, pk):
    item = get_object_or_404(CatalogoBazar, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item removido do catálogo.')
    return redirect('bazar:catalogo_listagem')


# ── Estoque ────────────────────────────────────────────────────────────────────

@login_required
@bazar_required
def estoque_listagem(request):
    itens = ItemEstoqueBazar.objects.select_related('catalogo').all()
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
                                    catalogo=item.catalogo,
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
    show_financial = _pode_ver_financeiro(request.user)
    total_geral = vendas.aggregate(total=Sum('valor_total'))['total'] or 0 if show_financial else None
    return render(request, 'bazar/vendas/listagem.html', {
        'vendas': vendas,
        'total_geral': total_geral,
        'show_financial': show_financial,
    })


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
                    venda.paroquia = request.user.paroquia
                    item = venda.item
                    if item.quantidade < venda.quantidade:
                        messages.error(request, f'Estoque insuficiente. Disponível: {item.quantidade}.')
                        return render(request, 'bazar/vendas/registrar.html', {'form': form})
                    item.quantidade -= venda.quantidade
                    item.save()
                    venda.save()
                    ano = timezone.now().year
                    venda.numero_operacao = f"{ano}-{venda.pk:05d}"
                    venda.save(update_fields=['numero_operacao'])
                    messages.success(request, f'Venda #{venda.numero_operacao} registrada!')
                    return redirect('bazar:comprovante', pk=venda.pk)
            except Exception as e:
                messages.error(request, f'Erro ao registrar venda: {str(e)}')
    else:
        form = VendaForm()
    itens_qs = ItemEstoqueBazar.objects.filter(quantidade__gt=0).select_related('catalogo')
    itens_json = json.dumps({
        str(i.pk): {'cat': i.catalogo_id, 'qty': i.quantidade, 'preco': float(i.preco_sugerido)}
        for i in itens_qs
    })
    return render(request, 'bazar/vendas/registrar.html', {'form': form, 'itens_json': itens_json})


@login_required
@bazar_required
def comprovante(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'bazar/comprovante.html', {'venda': venda})


@login_required
@bazar_required
def comprovante_pdf(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    template = get_template('bazar/pdf_comprovante.html')
    html = template.render({'venda': venda})

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF.', status=500)

    buffer.seek(0)
    filename = f"nota-venda-{venda.numero_operacao or venda.pk}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


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

    # Histórico dos últimos 6 meses
    abs_month = ano * 12 + (mes - 1)
    hist_labels, hist_vendas, hist_doacoes = [], [], []
    for i in range(5, -1, -1):
        t = abs_month - i
        a_h, m_h = t // 12, (t % 12) + 1
        ven_h = Venda.objects.filter(data__month=m_h, data__year=a_h).aggregate(
            total=Sum('valor_total'))['total'] or 0
        ent_h = EntradaBazar.objects.filter(
            data__month=m_h, data__year=a_h, tipo_entrada='doacao_financeira'
        ).aggregate(total=Sum('valor'))['total'] or 0
        hist_labels.append(f"{MESES_PT[m_h][:3]}/{str(a_h)[2:]}")
        hist_vendas.append(float(ven_h))
        hist_doacoes.append(float(ent_h))

    contexto = {
        'receita_vendas': vendas_mes.aggregate(total=Sum('valor_total'))['total'] or 0,
        'qtd_vendas': vendas_mes.count(),
        'receita_financeira': entradas_mes.filter(tipo_entrada='doacao_financeira').aggregate(total=Sum('valor'))['total'] or 0,
        'qtd_doacoes_item': entradas_mes.filter(tipo_entrada='doacao_item').count(),
        'itens_mais_vendidos': ItemEstoqueBazar.objects.annotate(
            total_vendido=Sum('vendas__quantidade')
        ).order_by('-total_vendido')[:5],
        'vendas_mes': vendas_mes.select_related('item'),
        'mes_atual': f"{MESES_PT[hoje.month]} de {hoje.year}",
        'hist_labels': json.dumps(hist_labels),
        'hist_vendas': json.dumps(hist_vendas),
        'hist_doacoes': json.dumps(hist_doacoes),
    }
    return render(request, 'bazar/relatorios/index.html', contexto)
