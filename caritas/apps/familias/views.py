from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import redirect, render

from .forms import DependenteForm, FamiliaForm
from .models import Familia


@login_required
def dashboard(request):
    total_familias = Familia.objects.count()
    return render(request, 'familias/dashboard.html', {'total_familias': total_familias})


@login_required
def cadastrar_familia(request):
    DependenteFormSet = formset_factory(DependenteForm, min_num=0, max_num=10, extra=1)

    if request.method == 'POST':
        form = FamiliaForm(request.POST)
        formset = DependenteFormSet(request.POST, prefix='dependentes')

        if form.is_valid() and formset.is_valid():
            familia = form.save(commit=False)
            familia.criado_por = request.user
            familia.save()

            for dep_form in formset:
                if dep_form.cleaned_data and not dep_form.cleaned_data.get('DELETE', False):
                    dependente = dep_form.save(commit=False)
                    dependente.familia = familia
                    dependente.save()

            messages.success(request, 'Família cadastrada com sucesso!')
            return redirect('familias:dashboard')
    else:
        form = FamiliaForm()
        formset = DependenteFormSet(prefix='dependentes')

    return render(request, 'familias/cadastro.html', {'form': form, 'formset': formset})
