from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Atendimento
from .forms import AtendimentoForm


@login_required
def listagem(request):
    atendimentos = Atendimento.objects.filter(
        paroquia=request.user.paroquia
    ).select_related('familia', 'registrado_por')
    return render(request, 'atendimentos/listagem.html', {'atendimentos': atendimentos})


@login_required
def registrar(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, paroquia=request.user.paroquia)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.paroquia = request.user.paroquia or 'Paróquia Padrão'
            atendimento.registrado_por = request.user
            atendimento.save()
            messages.success(request, 'Atendimento registrado com sucesso!')
            return redirect('atendimentos:listagem')
    else:
        form = AtendimentoForm(paroquia=request.user.paroquia)
    return render(request, 'atendimentos/registrar.html', {'form': form})
