import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from apps.accounts.decorators import modulo_paroquia_required
from apps.estoque.models import ItemEstoque
from .models import Atendimento, TIPOS_COM_ITENS
from .forms import AtendimentoForm, ItemAtendimentoFormSet

TIPO_CATEGORIA_MAP = {
    'doacao_roupas': ['roupa', 'calcado'],
    'doacao_cesta_basica': ['alimento'],
}


def _build_itens_json(paroquia):
    """JSON com opções de itens agrupadas por tipo de atendimento para filtro JS."""
    todos = ItemEstoque.objects.filter(paroquia=paroquia, quantidade__gt=0).order_by('nome', 'validade')

    def label(obj):
        l = obj.nome
        if obj.validade:
            l += f' — vence {obj.validade.strftime("%d/%m/%Y")}'
        l += f' ({obj.quantidade} {obj.unidade})'
        return l

    result = {}
    for tipo, cats in TIPO_CATEGORIA_MAP.items():
        result[tipo] = [{'v': str(i.pk), 't': label(i)} for i in todos.filter(categoria__in=cats)]
    return json.dumps(result)


@login_required
@modulo_paroquia_required
def listagem(request):
    atendimentos = Atendimento.objects.filter(
        paroquia=request.user.paroquia
    ).select_related('familia', 'registrado_por')
    return render(request, 'atendimentos/listagem.html', {'atendimentos': atendimentos})


@login_required
@modulo_paroquia_required
def registrar(request):
    paroquia = request.user.paroquia
    tipo_post = request.POST.get('tipo') if request.method == 'POST' else None
    categoria = TIPO_CATEGORIA_MAP.get(tipo_post)

    if request.method == 'POST':
        form = AtendimentoForm(request.POST, paroquia=paroquia)
        formset = ItemAtendimentoFormSet(request.POST, prefix='itens', paroquia=paroquia, categoria=categoria)

        if form.is_valid():
            tipo = form.cleaned_data['tipo']

            if tipo in TIPOS_COM_ITENS:
                if not formset.is_valid():
                    return render(request, 'atendimentos/registrar.html', {
                        'form': form, 'formset': formset,
                        'tipos_com_itens': TIPOS_COM_ITENS,
                    })
                itens_validos = [
                    f for f in formset
                    if f.cleaned_data and not f.cleaned_data.get('DELETE')
                ]
                if not itens_validos:
                    messages.error(request, 'Adicione pelo menos um item para este tipo de atendimento.')
                    return render(request, 'atendimentos/registrar.html', {
                        'form': form, 'formset': formset,
                        'tipos_com_itens': TIPOS_COM_ITENS,
                    })
                try:
                    with transaction.atomic():
                        atendimento = form.save(commit=False)
                        atendimento.paroquia = paroquia
                        atendimento.registrado_por = request.user
                        atendimento.save()

                        from .models import ItemAtendimento
                        for item_form in itens_validos:
                            item_estoque = item_form.cleaned_data['item_estoque']
                            quantidade = item_form.cleaned_data['quantidade']
                            if item_estoque.quantidade < quantidade:
                                raise ValueError(
                                    f'Estoque insuficiente para {item_estoque.nome}. '
                                    f'Disponível: {item_estoque.quantidade}.'
                                )
                            ItemAtendimento.objects.create(
                                atendimento=atendimento,
                                item_estoque=item_estoque,
                                item_nome=item_estoque.nome,
                                item_unidade=item_estoque.unidade,
                                quantidade=quantidade,
                            )
                            item_estoque.quantidade -= quantidade
                            item_estoque.save()

                        messages.success(request, 'Atendimento registrado e estoque atualizado!')
                        return redirect('atendimentos:listagem')
                except ValueError as e:
                    messages.error(request, str(e))
            else:
                atendimento = form.save(commit=False)
                atendimento.paroquia = paroquia
                atendimento.registrado_por = request.user
                atendimento.save()
                if tipo == 'encaminhamento' and atendimento.paroquia_destino:
                    familia = atendimento.familia
                    familia.paroquia_responsavel = atendimento.paroquia_destino
                    familia.save()
                messages.success(request, 'Atendimento registrado com sucesso!')
                return redirect('atendimentos:listagem')
    else:
        initial = {}
        familia_pk = request.GET.get('familia')
        if familia_pk:
            initial['familia'] = familia_pk
        form = AtendimentoForm(paroquia=paroquia, initial=initial)
        formset = ItemAtendimentoFormSet(prefix='itens', paroquia=paroquia)

    return render(request, 'atendimentos/registrar.html', {
        'form': form,
        'formset': formset,
        'tipos_com_itens': TIPOS_COM_ITENS,
        'itens_json': _build_itens_json(paroquia),
        'tipo_categoria_json': json.dumps(TIPO_CATEGORIA_MAP),
    })
