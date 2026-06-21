from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from apps.accounts.decorators import coordenador_required
from .models import MovimentacaoFinanceira
from .forms import MovimentacaoFinanceiraForm


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

    contexto = {
        'movimentacoes': qs,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': total_entradas - total_saidas,
        'mes_atual': hoje.strftime('%B de %Y'),
    }
    return render(request, 'financeiro/relatorio.html', contexto)
