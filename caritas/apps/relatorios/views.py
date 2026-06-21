import json
from django.db import models
from django.db.models import Sum, Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.accounts.decorators import coordenador_required
from apps.atendimentos.models import Atendimento
from apps.doacoes.models import Doacao
from apps.estoque.models import ItemEstoque
from apps.familias.models import Familia

MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}


TIPO_ATENDIMENTO_LABELS = dict([
    ('assistencia_social', 'Assistência Social'),
    ('doacao_roupas', 'Doação de Roupas'),
    ('doacao_cesta_basica', 'Doação de Cesta Básica'),
    ('encaminhamento', 'Encaminhamento'),
    ('visita_domiciliar', 'Visita Domiciliar'),
    ('outro', 'Outro'),
])


@login_required
@coordenador_required
def index(request):
    is_admin = request.user.perfil == 'administrador'
    paroquia = request.user.paroquia
    hoje = timezone.now().date()
    mes, ano = hoje.month, hoje.year

    def qs_paroquia(qs, campo='paroquia'):
        return qs if is_admin else qs.filter(**{campo: paroquia})

    # Famílias
    familias_qs = qs_paroquia(Familia.objects.all(), campo='paroquia_responsavel')
    total_familias = familias_qs.count()
    familias_bolsa = familias_qs.filter(bolsa_familia=True).count()

    # Estoque
    estoque_qs = qs_paroquia(ItemEstoque.objects.all())
    total_estoque_itens = estoque_qs.count()
    total_estoque_qtd = estoque_qs.aggregate(total=Sum('quantidade'))['total'] or 0
    itens_vencidos = [i for i in estoque_qs if i.esta_vencido()]
    itens_vence_breve = [i for i in estoque_qs if i.vence_em_breve()]

    # Doações do mês
    doacoes_mes = qs_paroquia(
        Doacao.objects.filter(data__month=mes, data__year=ano).prefetch_related('itens')
    )

    # Atendimentos do mês
    atendimentos_qs = qs_paroquia(
        Atendimento.objects.filter(data__month=mes, data__year=ano)
    )
    atendimentos_por_tipo_raw = atendimentos_qs.values('tipo').annotate(total=Count('id'))
    atendimentos_por_tipo = [
        {'label': TIPO_ATENDIMENTO_LABELS.get(r['tipo'], r['tipo']), 'total': r['total']}
        for r in atendimentos_por_tipo_raw
    ]

    # Histórico dos últimos 6 meses
    abs_month = hoje.year * 12 + (hoje.month - 1)
    hist_labels, hist_atendimentos, hist_doacoes = [], [], []
    for i in range(5, -1, -1):
        t = abs_month - i
        a_h, m_h = t // 12, (t % 12) + 1
        if is_admin:
            at_c = Atendimento.objects.filter(data__month=m_h, data__year=a_h).count()
            do_c = Doacao.objects.filter(data__month=m_h, data__year=a_h).count()
        else:
            at_c = Atendimento.objects.filter(paroquia=paroquia, data__month=m_h, data__year=a_h).count()
            do_c = Doacao.objects.filter(paroquia=paroquia, data__month=m_h, data__year=a_h).count()
        hist_labels.append(f"{MESES_PT[m_h][:3]}/{str(a_h)[2:]}")
        hist_atendimentos.append(at_c)
        hist_doacoes.append(do_c)

    # Dados do gráfico de pizza por tipo
    tipo_labels = [r['label'] for r in atendimentos_por_tipo]
    tipo_totais = [r['total'] for r in atendimentos_por_tipo]

    contexto = {
        'is_admin': is_admin,
        'paroquia': paroquia,
        'mes_atual': f"{MESES_PT[hoje.month]} de {hoje.year}",
        'total_familias': total_familias,
        'familias_bolsa': familias_bolsa,
        'total_estoque_itens': total_estoque_itens,
        'total_estoque_qtd': total_estoque_qtd,
        'itens_vencidos': itens_vencidos,
        'itens_vence_breve': itens_vence_breve,
        'doacoes_mes': doacoes_mes,
        'atendimentos_mes': atendimentos_qs,
        'atendimentos_por_tipo': atendimentos_por_tipo,
        'hist_labels': json.dumps(hist_labels),
        'hist_atendimentos': json.dumps(hist_atendimentos),
        'hist_doacoes': json.dumps(hist_doacoes),
        'tipo_labels': json.dumps(tipo_labels),
        'tipo_totais': json.dumps(tipo_totais),
    }
    return render(request, 'relatorios/index.html', contexto)
