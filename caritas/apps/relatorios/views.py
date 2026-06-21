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
    }
    return render(request, 'relatorios/index.html', contexto)
