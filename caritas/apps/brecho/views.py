from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.accounts.decorators import coordenador_required
from .models import BrechoEvento, VendaBrecho
from .forms import BrechoEventoForm, VendaBrechoForm


@login_required
def listagem(request):
    eventos = BrechoEvento.objects.filter(paroquia=request.user.paroquia)
    return render(request, 'brecho/listagem.html', {'eventos': eventos})


@login_required
@coordenador_required
def criar_evento(request):
    if request.method == 'POST':
        form = BrechoEventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.paroquia = request.user.paroquia or 'Paróquia Padrão'
            evento.criado_por = request.user
            evento.save()
            messages.success(request, 'Evento de brechó criado!')
            return redirect('brecho:detalhe', pk=evento.pk)
    else:
        form = BrechoEventoForm()
    return render(request, 'brecho/form_evento.html', {'form': form, 'titulo': 'Novo Brechó'})


@login_required
def detalhe(request, pk):
    evento = get_object_or_404(BrechoEvento, pk=pk, paroquia=request.user.paroquia)
    vendas = evento.vendas.select_related('item_estoque', 'registrado_por')
    return render(request, 'brecho/detalhe.html', {'evento': evento, 'vendas': vendas})


@login_required
def registrar_venda(request, pk):
    evento = get_object_or_404(BrechoEvento, pk=pk, paroquia=request.user.paroquia)
    if evento.status == 'encerrado':
        messages.error(request, 'Este brechó já foi encerrado.')
        return redirect('brecho:detalhe', pk=pk)

    if request.method == 'POST':
        form = VendaBrechoForm(request.POST, paroquia=request.user.paroquia)
        if form.is_valid():
            try:
                with transaction.atomic():
                    venda = form.save(commit=False)
                    venda.evento = evento
                    venda.registrado_por = request.user

                    item = venda.item_estoque
                    if item.quantidade < venda.quantidade:
                        messages.error(request, f'Estoque insuficiente. Disponível: {item.quantidade}.')
                        return render(request, 'brecho/registrar_venda.html', {'form': form, 'evento': evento})

                    item.quantidade -= venda.quantidade
                    item.save()
                    venda.save()
                    messages.success(request, 'Venda registrada e estoque atualizado!')
                    return redirect('brecho:detalhe', pk=pk)
            except Exception as e:
                messages.error(request, f'Erro ao registrar venda: {str(e)}')
    else:
        form = VendaBrechoForm(paroquia=request.user.paroquia)
    return render(request, 'brecho/registrar_venda.html', {'form': form, 'evento': evento})


@login_required
@coordenador_required
def encerrar_evento(request, pk):
    evento = get_object_or_404(BrechoEvento, pk=pk, paroquia=request.user.paroquia)
    evento.status = 'encerrado'
    evento.save()
    messages.success(request, f'Brechó "{evento.nome}" encerrado.')
    return redirect('brecho:detalhe', pk=pk)
