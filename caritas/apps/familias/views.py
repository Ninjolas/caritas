from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DependenteForm, FamiliaForm
from .models import Dependente, Familia


@login_required
def dashboard(request):
    from apps.estoque.models import ItemEstoque
    from apps.doacoes.models import Doacao

    paroquia = request.user.paroquia or 'Paróquia Padrão'
    hoje = date.today()

    if request.user.perfil == 'administrador':
        total_familias = Familia.objects.count()
        total_estoque = ItemEstoque.objects.count()
        total_doacoes_mes = Doacao.objects.filter(data__month=hoje.month).count()
    else:
        total_familias = Familia.objects.filter(paroquia_responsavel=paroquia).count()
        total_estoque = ItemEstoque.objects.filter(paroquia=paroquia).count()
        total_doacoes_mes = Doacao.objects.filter(paroquia=paroquia, data__month=hoje.month).count()

    return render(request, 'familias/dashboard.html', {
        'total_familias': total_familias,
        'total_estoque': total_estoque,
        'total_doacoes_mes': total_doacoes_mes,
    })


@login_required
def listar_familias(request):
    familias = Familia.objects.all().order_by('paroquia_responsavel', 'responsavel_nome')
    paroquia_usuario = request.user.paroquia
    is_admin = request.user.perfil == 'administrador'
    return render(request, 'familias/listagem.html', {
        'familias': familias,
        'paroquia_usuario': paroquia_usuario,
        'is_admin': is_admin,
    })


@login_required
def detalhe_familia(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    return render(request, 'familias/detalhe.html', {'familia': familia})


@login_required
def editar_familia(request, pk):
    familia = get_object_or_404(Familia, pk=pk)
    if request.user.perfil != 'administrador' and familia.paroquia_responsavel != request.user.paroquia:
        raise PermissionDenied

    DependenteFormSet = inlineformset_factory(
        Familia, Dependente, form=DependenteForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = FamiliaForm(request.POST, instance=familia)
        formset = DependenteFormSet(request.POST, instance=familia, prefix='dependentes')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Família atualizada com sucesso!')
            return redirect('familias:listar_familias')
    else:
        form = FamiliaForm(instance=familia)
        formset = DependenteFormSet(instance=familia, prefix='dependentes')

    return render(request, 'familias/editar.html', {
        'form': form,
        'formset': formset,
        'familia': familia,
    })


@login_required
def cadastrar_familia(request):
    DependenteFormSet = formset_factory(DependenteForm, min_num=0, max_num=10, extra=1)

    if request.method == 'POST':
        form = FamiliaForm(request.POST)
        formset = DependenteFormSet(request.POST, prefix='dependentes')

        if form.is_valid() and formset.is_valid():
            familia = form.save(commit=False)
            familia.criado_por = request.user
            familia.paroquia_responsavel = request.user.paroquia or 'Paróquia Padrão'
            familia.save()

            for dep_form in formset:
                if dep_form.cleaned_data and not dep_form.cleaned_data.get('DELETE', False):
                    dependente = dep_form.save(commit=False)
                    dependente.familia = familia
                    dependente.save()

            messages.success(request, 'Família cadastrada com sucesso!')
            return redirect('familias:listar_familias')
    else:
        form = FamiliaForm()
        formset = DependenteFormSet(prefix='dependentes')

    return render(request, 'familias/cadastro.html', {'form': form, 'formset': formset})
