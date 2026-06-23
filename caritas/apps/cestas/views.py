import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from apps.accounts.decorators import coordenador_required, modulo_paroquia_required
from apps.estoque.models import ItemEstoque
from .models import (
    CestaRecebida, ItemCestaRecebida,
    CestaEntregue, ItemCestaEntregue,
    ModeloCesta, ModeloItemCesta,
)
from .forms import (
    CestaRecebidaForm, ItemCestaRecebidaFormSet,
    CestaEntregueForm, CestaEntregueEditarForm, ItemCestaEntregueFormSet,
    ModeloCestaForm, ModeloItemCestaInlineFormSet,
)


def _check_paroquia(user, obj_paroquia):
    if user.perfil != 'administrador' and obj_paroquia != user.paroquia:
        raise PermissionDenied


# ── Listagem ───────────────────────────────────────────────────────────────────

@login_required
@modulo_paroquia_required
def listagem(request):
    is_admin = request.user.perfil == 'administrador'
    paroquia = request.user.paroquia
    if is_admin:
        recebidas = CestaRecebida.objects.prefetch_related('itens').select_related('paroquia', 'registrado_por').all()
        entregues = CestaEntregue.objects.select_related('familia', 'paroquia', 'modelo_usado', 'registrado_por').prefetch_related('itens').all()
    else:
        recebidas = CestaRecebida.objects.filter(paroquia=paroquia).prefetch_related('itens').select_related('registrado_por')
        entregues = CestaEntregue.objects.filter(paroquia=paroquia).select_related('familia', 'modelo_usado', 'registrado_por').prefetch_related('itens')
    return render(request, 'cestas/listagem.html', {
        'recebidas': recebidas,
        'entregues': entregues,
        'is_admin': is_admin,
    })


# ── Receber cesta ──────────────────────────────────────────────────────────────

@login_required
@modulo_paroquia_required
def receber(request):
    paroquia = request.user.paroquia
    if request.method == 'POST':
        form = CestaRecebidaForm(request.POST)
        formset = ItemCestaRecebidaFormSet(request.POST, prefix='itens')
        if form.is_valid() and formset.is_valid():
            itens_validos = [f for f in formset if f.cleaned_data and not f.cleaned_data.get('DELETE')]
            if not itens_validos:
                messages.error(request, 'Adicione ao menos um item à cesta.')
            else:
                try:
                    with transaction.atomic():
                        cesta = form.save(commit=False)
                        cesta.paroquia = paroquia
                        cesta.registrado_por = request.user
                        cesta.save()
                        for item_form in itens_validos:
                            d = item_form.cleaned_data
                            ItemCestaRecebida.objects.create(
                                cesta=cesta, nome=d['nome'],
                                quantidade=d['quantidade'], unidade=d['unidade'],
                                validade=d.get('validade'),
                            )
                            ItemEstoque.objects.create(
                                paroquia=paroquia, nome=d['nome'],
                                categoria='alimento', quantidade=d['quantidade'],
                                unidade=d['unidade'], validade=d.get('validade'),
                                registrado_por=request.user,
                            )
                        messages.success(request, 'Cesta recebida registrada e itens adicionados ao estoque!')
                        return redirect('cestas:listagem')
                except Exception as e:
                    messages.error(request, f'Erro ao registrar cesta: {str(e)}')
    else:
        form = CestaRecebidaForm()
        formset = ItemCestaRecebidaFormSet(prefix='itens')
    return render(request, 'cestas/receber.html', {'form': form, 'formset': formset})


@login_required
@coordenador_required
def editar_recebida(request, pk):
    cesta = get_object_or_404(CestaRecebida, pk=pk)
    _check_paroquia(request.user, cesta.paroquia)
    if request.method == 'POST':
        form = CestaRecebidaForm(request.POST, instance=cesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cesta recebida atualizada.')
            return redirect('cestas:listagem')
    else:
        form = CestaRecebidaForm(instance=cesta)
    return render(request, 'cestas/editar_recebida.html', {'form': form, 'cesta': cesta})


@login_required
@coordenador_required
def remover_recebida(request, pk):
    cesta = get_object_or_404(CestaRecebida, pk=pk)
    _check_paroquia(request.user, cesta.paroquia)
    if request.method == 'POST':
        with transaction.atomic():
            for item in cesta.itens.all():
                filtro = {'paroquia': cesta.paroquia, 'validade': item.validade}
                if item.produto:
                    filtro['produto'] = item.produto
                else:
                    filtro['nome'] = item.nome
                item_estoque = ItemEstoque.objects.filter(**filtro).first()
                if item_estoque:
                    item_estoque.quantidade -= item.quantidade
                    item_estoque.save()
            cesta.delete()
        messages.success(request, 'Cesta recebida removida e estoque revertido.')
        return redirect('cestas:listagem')
    return render(request, 'cestas/remover_recebida.html', {'cesta': cesta})


# ── Montar/entregar cesta ──────────────────────────────────────────────────────

@login_required
@modulo_paroquia_required
def montar(request):
    paroquia = request.user.paroquia
    modelos_json = {
        str(m.pk): [
            {'nome': i.nome.lower(), 'quantidade': i.quantidade, 'unidade': i.unidade}
            for i in m.itens.all()
        ]
        for m in ModeloCesta.objects.prefetch_related('itens').all()
    }
    qs_estoque = ItemEstoque.objects.filter(
        paroquia=paroquia, quantidade__gt=0, categoria='alimento'
    ).order_by('nome', 'validade')
    itens_estoque_json = {
        str(i.pk): {'nome': i.nome.lower(), 'qtd': i.quantidade, 'unidade': i.unidade}
        for i in qs_estoque
    }

    if request.method == 'POST':
        form = CestaEntregueForm(request.POST, paroquia=paroquia)
        formset = ItemCestaEntregueFormSet(request.POST, prefix='itens', paroquia=paroquia)
        if form.is_valid() and formset.is_valid():
            itens_validos = [f for f in formset if f.cleaned_data and not f.cleaned_data.get('DELETE')]
            if not itens_validos:
                messages.error(request, 'Adicione ao menos um item à cesta.')
            else:
                try:
                    with transaction.atomic():
                        cesta = form.save(commit=False)
                        cesta.paroquia = paroquia
                        cesta.registrado_por = request.user
                        cesta.save()
                        for item_form in itens_validos:
                            d = item_form.cleaned_data
                            item_est = d['item_estoque']
                            qtd = d['quantidade']
                            if item_est.quantidade < qtd:
                                raise ValueError(
                                    f'Estoque insuficiente para {item_est.nome}. '
                                    f'Disponivel: {item_est.quantidade}.'
                                )
                            ItemCestaEntregue.objects.create(
                                cesta=cesta, item_estoque=item_est,
                                item_nome=item_est.nome, item_unidade=item_est.unidade,
                                quantidade=qtd,
                            )
                            item_est.quantidade -= qtd
                            item_est.save()
                        messages.success(
                            request,
                            f'Cesta entregue a {cesta.familia.responsavel_nome} e estoque atualizado!'
                        )
                        return redirect('cestas:listagem')
                except ValueError as e:
                    messages.error(request, str(e))
                except Exception as e:
                    messages.error(request, f'Erro ao registrar cesta: {str(e)}')
    else:
        form = CestaEntregueForm(paroquia=paroquia)
        formset = ItemCestaEntregueFormSet(prefix='itens', paroquia=paroquia)
    return render(request, 'cestas/montar.html', {
        'form': form,
        'formset': formset,
        'modelos_json': json.dumps(modelos_json),
        'itens_estoque_json': json.dumps(itens_estoque_json),
    })


@login_required
@coordenador_required
def editar_entregue(request, pk):
    cesta = get_object_or_404(CestaEntregue, pk=pk)
    _check_paroquia(request.user, cesta.paroquia)
    if request.method == 'POST':
        form = CestaEntregueEditarForm(request.POST, instance=cesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cesta entregue atualizada.')
            return redirect('cestas:listagem')
    else:
        form = CestaEntregueEditarForm(instance=cesta)
    return render(request, 'cestas/editar_entregue.html', {'form': form, 'cesta': cesta})


@login_required
@coordenador_required
def remover_entregue(request, pk):
    cesta = get_object_or_404(CestaEntregue, pk=pk)
    _check_paroquia(request.user, cesta.paroquia)
    if request.method == 'POST':
        with transaction.atomic():
            for item in cesta.itens.select_related('item_estoque').all():
                if item.item_estoque:
                    item.item_estoque.quantidade += item.quantidade
                    item.item_estoque.save()
            cesta.delete()
        messages.success(request, 'Cesta entregue removida e estoque restaurado.')
        return redirect('cestas:listagem')
    return render(request, 'cestas/remover_entregue.html', {'cesta': cesta})


# ── Modelos de cesta ───────────────────────────────────────────────────────────

@login_required
@coordenador_required
def modelo_listagem(request):
    modelos = ModeloCesta.objects.prefetch_related('itens').all()
    return render(request, 'cestas/modelos/listagem.html', {'modelos': modelos})


@login_required
@coordenador_required
def modelo_form(request, pk=None):
    modelo = get_object_or_404(ModeloCesta, pk=pk) if pk else None
    dummy = modelo or ModeloCesta()
    if request.method == 'POST':
        form = ModeloCestaForm(request.POST, instance=modelo)
        formset = ModeloItemCestaInlineFormSet(request.POST, instance=dummy)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                m = form.save(commit=False)
                if not pk:
                    m.paroquia = request.user.paroquia
                m.save()
                formset.instance = m
                formset.save()
            messages.success(request, f'Modelo "{m.nome}" salvo com sucesso!')
            return redirect('cestas:modelo_listagem')
    else:
        form = ModeloCestaForm(instance=modelo)
        formset = ModeloItemCestaInlineFormSet(instance=dummy)
    return render(request, 'cestas/modelos/form.html', {
        'form': form, 'formset': formset, 'modelo': modelo,
    })


@login_required
@coordenador_required
def modelo_remover(request, pk):
    modelo = get_object_or_404(ModeloCesta, pk=pk)
    if request.method == 'POST':
        nome = modelo.nome
        modelo.delete()
        messages.success(request, f'Modelo "{nome}" removido.')
        return redirect('cestas:modelo_listagem')
    return render(request, 'cestas/modelos/remover.html', {'modelo': modelo})
