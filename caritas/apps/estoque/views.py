from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ItemEstoque
from .forms import ItemEstoqueForm


@login_required
def listagem(request):
    paroquia = request.user.paroquia or 'Paróquia Padrão'
    itens = ItemEstoque.objects.filter(paroquia=paroquia)
    return render(request, 'estoque/listagem.html', {'itens': itens})


@login_required
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
