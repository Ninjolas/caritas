from django import forms
from django.forms import inlineformset_factory
from .models import CestaPronta, ItemMontagem, EntregaCesta
from apps.estoque.models import ItemEstoque
from apps.familias.models import Familia


class MontagemForm(forms.ModelForm):
    class Meta:
        model = CestaPronta
        fields = ['quantidade', 'data', 'observacao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ItemMontagemForm(forms.ModelForm):
    class Meta:
        model = ItemMontagem
        fields = ['item_estoque', 'quantidade_total']
        widgets = {
            'item_estoque': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            self.fields['item_estoque'].queryset = ItemEstoque.objects.filter(
                paroquia=paroquia,
                quantidade__gt=0,
            ).exclude(categoria='roupa')


_BaseItemMontagemFormSet = inlineformset_factory(
    CestaPronta, ItemMontagem,
    form=ItemMontagemForm,
    extra=1, min_num=1, validate_min=True, can_delete=True,
)


class ItemMontagemFormSet(_BaseItemMontagemFormSet):
    def __init__(self, *args, paroquia=None, **kwargs):
        self.paroquia = paroquia
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['paroquia'] = self.paroquia
        return super()._construct_form(i, **kwargs)


class DoacaoCestaForm(forms.ModelForm):
    class Meta:
        model = CestaPronta
        fields = ['quantidade', 'data', 'observacao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class EntregaCestaForm(forms.ModelForm):
    class Meta:
        model = EntregaCesta
        fields = ['familia', 'quantidade', 'data', 'observacao']
        widgets = {
            'familia': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            self.fields['familia'].queryset = Familia.objects.filter(
                paroquia_responsavel=paroquia
            ).order_by('responsavel_nome')
