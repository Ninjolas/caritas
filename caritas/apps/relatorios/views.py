from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.accounts.decorators import coordenador_required
from apps.familias.models import Familia
from apps.estoque.models import ItemEstoque
from apps.doacoes.models import Doacao
from apps.atendimentos.models import Atendimento


@login_required
@coordenador_required
def index(request):
    paroquia = request.user.paroquia
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    contexto = {
        'total_familias': Familia.objects.filter(paroquia_responsavel=paroquia).count(),
        'familias_bolsa': Familia.objects.filter(paroquia_responsavel=paroquia, bolsa_familia=True).count(),
        'total_estoque': ItemEstoque.objects.filter(paroquia=paroquia).count(),
        'itens_vencidos': [i for i in ItemEstoque.objects.filter(paroquia=paroquia) if i.esta_vencido()],
        'itens_vence_breve': [i for i in ItemEstoque.objects.filter(paroquia=paroquia) if i.vence_em_breve()],
        'doacoes_mes': Doacao.objects.filter(paroquia=paroquia, data__month=mes_atual, data__year=ano_atual),
        'atendimentos_mes': Atendimento.objects.filter(paroquia=paroquia, data__month=mes_atual, data__year=ano_atual),
        'atendimentos_por_tipo': Atendimento.objects.filter(
            paroquia=paroquia, data__month=mes_atual, data__year=ano_atual
        ).values('tipo').annotate(total=models.Count('id')),
        'mes_atual': hoje.strftime('%B de %Y'),
    }
    return render(request, 'relatorios/index.html', contexto)
