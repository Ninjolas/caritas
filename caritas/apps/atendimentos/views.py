from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from apps.accounts.decorators import modulo_paroquia_required
from .models import Atendimento, TIPOS_COM_ITENS
from .forms import AtendimentoForm, ItemAtendimentoFormSet


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

    if request.method == 'POST':
        form = AtendimentoForm(request.POST, paroquia=paroquia)
        formset = ItemAtendimentoFormSet(request.POST, prefix='itens', paroquia=paroquia)

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
                atendimento.paroquia = paroquia or 'Paróquia Padrão'
                atendimento.registrado_por = request.user
                atendimento.save()
                messages.success(request, 'Atendimento registrado com sucesso!')
                return redirect('atendimentos:listagem')
    else:
        form = AtendimentoForm(paroquia=paroquia)
        formset = ItemAtendimentoFormSet(prefix='itens', paroquia=paroquia)

    return render(request, 'atendimentos/registrar.html', {
        'form': form,
        'formset': formset,
        'tipos_com_itens': TIPOS_COM_ITENS,
    })
