from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.decorators import coordenador_required

from .forms import ItemEstoqueForm
from .models import ItemEstoque


@login_required
def listagem(request):
    if request.user.perfil == 'administrador':
        itens = ItemEstoque.objects.all().order_by('paroquia', 'nome')
    else:
        paroquia = request.user.paroquia or 'Paróquia Padrão'
        itens = ItemEstoque.objects.filter(paroquia=paroquia)
    return render(request, 'estoque/listagem.html', {'itens': itens})


@login_required
@coordenador_required
def entrada(request):
    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.paroquia = request.user.paroquia or 'Paróquia Padrão'
            item.registrado_por = request.user
            item.save()
            messages.success(request, 'Item registrado no estoque com sucesso!')
            return redirect('estoque:listagem')
    else:
        form = ItemEstoqueForm()
    return render(request, 'estoque/entrada.html', {'form': form})
