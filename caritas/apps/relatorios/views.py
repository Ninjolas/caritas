import csv
import json
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.accounts.decorators import coordenador_required
from apps.atendimentos.models import Atendimento
from apps.cestas.models import CestaEntregue, CestaRecebida
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
    ('encaminhamento', 'Encaminhamento'),
    ('visita_domiciliar', 'Visita Domiciliar'),
    ('outro', 'Outro'),
])


def _parse_mes_ano(request):
    hoje = timezone.now().date()
    try:
        mes = int(request.GET.get('mes', hoje.month))
        ano = int(request.GET.get('ano', hoje.year))
        if not (1 <= mes <= 12) or not (2000 <= ano <= 2100):
            raise ValueError
    except (ValueError, TypeError):
        mes, ano = hoje.month, hoje.year
    return mes, ano


def _nav_mes(mes, ano, delta):
    m = mes + delta
    a = ano
    if m < 1:
        m, a = 12, ano - 1
    elif m > 12:
        m, a = 1, ano + 1
    return m, a


def _build_context(request, mes, ano):
    is_admin = request.user.perfil == 'administrador'
    paroquia = request.user.paroquia

    def qs_par(qs, campo='paroquia'):
        return qs if is_admin else qs.filter(**{campo: paroquia})

    # Famílias
    familias_qs = qs_par(Familia.objects.all(), campo='paroquia_responsavel')

    # Estoque
    estoque_qs = qs_par(ItemEstoque.objects.all())
    itens_vencidos = [i for i in estoque_qs if i.esta_vencido()]
    itens_vence_breve = [i for i in estoque_qs if i.vence_em_breve()]

    # Doações do mês
    doacoes_mes = qs_par(
        Doacao.objects.filter(data__month=mes, data__year=ano).prefetch_related('itens')
    )

    # Atendimentos do mês
    atendimentos_qs = qs_par(
        Atendimento.objects.filter(data__month=mes, data__year=ano)
    )
    atendimentos_por_tipo_raw = atendimentos_qs.values('tipo').annotate(total=Count('id'))
    atendimentos_por_tipo = [
        {'label': TIPO_ATENDIMENTO_LABELS.get(r['tipo'], r['tipo']), 'total': r['total']}
        for r in atendimentos_por_tipo_raw
    ]

    # Cestas do mês
    cestas_entregues_mes = qs_par(
        CestaEntregue.objects.filter(data__month=mes, data__year=ano)
        .select_related('familia', 'modelo_usado').prefetch_related('itens')
    )
    cestas_recebidas_mes = qs_par(
        CestaRecebida.objects.filter(data__month=mes, data__year=ano)
        .prefetch_related('itens')
    )

    # Histórico últimos 6 meses
    hoje = timezone.now().date()
    abs_month = ano * 12 + (mes - 1)
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

    tipo_labels = [r['label'] for r in atendimentos_por_tipo]
    tipo_totais = [r['total'] for r in atendimentos_por_tipo]

    prev_mes, prev_ano = _nav_mes(mes, ano, -1)
    next_mes, next_ano = _nav_mes(mes, ano, +1)
    is_current = (mes == hoje.month and ano == hoje.year)

    anos_disponiveis = list(range(2023, hoje.year + 1))

    return {
        'is_admin': is_admin,
        'paroquia': paroquia,
        'mes': mes,
        'ano': ano,
        'mes_atual': f"{MESES_PT[mes]} de {ano}",
        'prev_mes': prev_mes, 'prev_ano': prev_ano,
        'next_mes': next_mes, 'next_ano': next_ano,
        'is_current_month': is_current,
        'mes_choices': list(MESES_PT.items()),
        'anos_disponiveis': anos_disponiveis,
        'total_familias': familias_qs.count(),
        'familias_bolsa': familias_qs.filter(bolsa_familia=True).count(),
        'total_estoque_itens': estoque_qs.count(),
        'total_estoque_qtd': estoque_qs.aggregate(total=Sum('quantidade'))['total'] or 0,
        'itens_vencidos': itens_vencidos,
        'itens_vence_breve': itens_vence_breve,
        'doacoes_mes': doacoes_mes,
        'atendimentos_mes': atendimentos_qs,
        'atendimentos_por_tipo': atendimentos_por_tipo,
        'cestas_entregues_mes': cestas_entregues_mes,
        'cestas_recebidas_mes': cestas_recebidas_mes,
        'hist_labels': json.dumps(hist_labels),
        'hist_atendimentos': json.dumps(hist_atendimentos),
        'hist_doacoes': json.dumps(hist_doacoes),
        'tipo_labels': json.dumps(tipo_labels),
        'tipo_totais': json.dumps(tipo_totais),
    }


@login_required
@coordenador_required
def index(request):
    mes, ano = _parse_mes_ano(request)
    ctx = _build_context(request, mes, ano)
    return render(request, 'relatorios/index.html', ctx)


@login_required
@coordenador_required
def download(request):
    mes, ano = _parse_mes_ano(request)
    ctx = _build_context(request, mes, ano)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename="relatorio_{MESES_PT[mes].lower()}_{ano}.csv"'
    )
    response.write('﻿')  # BOM for Excel

    w = csv.writer(response)
    nome_par = str(ctx['paroquia']) if not ctx['is_admin'] else 'Todas as paróquias'
    w.writerow([f'Relatório Cáritas — {ctx["mes_atual"]} — {nome_par}'])
    w.writerow([])

    w.writerow(['FAMÍLIAS'])
    w.writerow(['Total cadastradas', ctx['total_familias']])
    w.writerow(['Com Bolsa Família', ctx['familias_bolsa']])
    w.writerow([])

    w.writerow(['ESTOQUE'])
    w.writerow(['Tipos de item', ctx['total_estoque_itens']])
    w.writerow(['Unidades totais', ctx['total_estoque_qtd']])
    w.writerow(['Itens vencidos', len(ctx['itens_vencidos'])])
    w.writerow(['Vencem em até 7 dias', len(ctx['itens_vence_breve'])])
    w.writerow([])

    w.writerow(['ATENDIMENTOS DO MÊS'])
    w.writerow(['Total', ctx['atendimentos_mes'].count()])
    for item in ctx['atendimentos_por_tipo']:
        w.writerow([item['label'], item['total']])
    w.writerow([])

    w.writerow(['DOAÇÕES RECEBIDAS DO MÊS'])
    w.writerow(['Data', 'Doador', 'Itens'])
    for d in ctx['doacoes_mes']:
        w.writerow([d.data.strftime('%d/%m/%Y'), d.doador, d.itens.count()])
    w.writerow([])

    w.writerow(['CESTAS BÁSICAS — RECEBIDAS NO MÊS'])
    w.writerow(['Data', 'Doador', 'Itens'])
    for c in ctx['cestas_recebidas_mes']:
        w.writerow([c.data.strftime('%d/%m/%Y'), c.doador_nome or 'Anônimo', c.itens.count()])
    w.writerow([])

    w.writerow(['CESTAS BÁSICAS — ENTREGUES NO MÊS'])
    w.writerow(['Data', 'Família', 'Itens'])
    for c in ctx['cestas_entregues_mes']:
        w.writerow([c.data.strftime('%d/%m/%Y'), c.familia.responsavel_nome, c.itens.count()])

    return response
