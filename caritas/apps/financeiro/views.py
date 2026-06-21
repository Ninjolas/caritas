import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from apps.accounts.decorators import coordenador_required
from .models import MovimentacaoFinanceira
from .forms import MovimentacaoFinanceiraForm

MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}


@login_required
@coordenador_required
def listagem(request):
    paroquia = request.user.paroquia
    if request.user.perfil == 'administrador':
        movimentacoes = MovimentacaoFinanceira.objects.all()
    else:
        movimentacoes = MovimentacaoFinanceira.objects.filter(origem='paroquia', paroquia=paroquia)
    return render(request, 'financeiro/listagem.html', {'movimentacoes': movimentacoes})


@login_required
@coordenador_required
def registrar(request):
    if request.method == 'POST':
        form = MovimentacaoFinanceiraForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            if request.user.perfil == 'administrador':
                mov.origem = 'diocese'
                mov.paroquia = None
            else:
                mov.origem = 'paroquia'
                mov.paroquia = request.user.paroquia
            mov.registrado_por = request.user
            mov.save()
            messages.success(request, 'Movimentação registrada!')
            return redirect('financeiro:listagem')
    else:
        form = MovimentacaoFinanceiraForm()
    return render(request, 'financeiro/form.html', {'form': form})


@login_required
@coordenador_required
def relatorio(request):
    hoje = timezone.now().date()
    mes, ano = hoje.month, hoje.year
    paroquia = request.user.paroquia

    if request.user.perfil == 'administrador':
        qs = MovimentacaoFinanceira.objects.filter(data__month=mes, data__year=ano)
    else:
        qs = MovimentacaoFinanceira.objects.filter(
            origem='paroquia', paroquia=paroquia,
            data__month=mes, data__year=ano,
        )

    total_entradas = qs.filter(tipo__startswith='entrada').aggregate(total=Sum('valor'))['total'] or 0
    total_saidas = qs.filter(tipo__startswith='saida').aggregate(total=Sum('valor'))['total'] or 0

    # Histórico dos últimos 6 meses
    abs_month = ano * 12 + (mes - 1)
    hist_labels, hist_entradas, hist_saidas = [], [], []
    for i in range(5, -1, -1):
        t = abs_month - i
        a_h, m_h = t // 12, (t % 12) + 1
        if request.user.perfil == 'administrador':
            qs_h = MovimentacaoFinanceira.objects.filter(data__month=m_h, data__year=a_h)
        else:
            qs_h = MovimentacaoFinanceira.objects.filter(origem='paroquia', paroquia=paroquia, data__month=m_h, data__year=a_h)
        ent_h = qs_h.filter(tipo__startswith='entrada').aggregate(t=Sum('valor'))['t'] or 0
        sai_h = qs_h.filter(tipo__startswith='saida').aggregate(t=Sum('valor'))['t'] or 0
        hist_labels.append(f"{MESES_PT[m_h][:3]}/{str(a_h)[2:]}")
        hist_entradas.append(float(ent_h))
        hist_saidas.append(float(sai_h))

    contexto = {
        'movimentacoes': qs,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': total_entradas - total_saidas,
        'mes_atual': f"{MESES_PT[mes]} de {ano}",
        'hist_labels': json.dumps(hist_labels),
        'hist_entradas': json.dumps(hist_entradas),
        'hist_saidas': json.dumps(hist_saidas),
    }
    return render(request, 'financeiro/relatorio.html', contexto)
