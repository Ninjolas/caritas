import json
from django import forms
from django.forms import inlineformset_factory
from .models import CestaPronta, ItemMontagem, EntregaCesta
from apps.estoque.models import ItemEstoque
from apps.familias.models import Familia


class ItemEstoqueComEstoqueField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} ({obj.unidade}) — {obj.quantidade} disponíveis"


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
    item_estoque = ItemEstoqueComEstoqueField(
        queryset=ItemEstoque.objects.none(),
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select item-estoque-select'}),
        label='Item do estoque',
    )

    class Meta:
        model = ItemMontagem
        fields = ['item_estoque', 'quantidade_total']
        widgets = {
            'quantidade_total': forms.NumberInput(attrs={
                'class': 'form-control quantidade-input', 'min': 1
            }),
        }
        labels = {
            'quantidade_total': 'Quantidade',
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            qs = ItemEstoque.objects.filter(
                paroquia=paroquia, quantidade__gt=0,
            ).exclude(categoria='roupa').order_by('nome')
        else:
            qs = ItemEstoque.objects.none()
        self.fields['item_estoque'].queryset = qs
        # Inject stock map as JSON into the select widget for JS validation
        stocks = {str(item.pk): item.quantidade for item in qs}
        self.fields['item_estoque'].widget.attrs['data-stocks'] = json.dumps(stocks)

    def clean(self):
        cleaned = super().clean()
        item = cleaned.get('item_estoque')
        qtd = cleaned.get('quantidade_total')
        if item and qtd and qtd > item.quantidade:
            raise forms.ValidationError(
                f'Estoque insuficiente para "{item.nome}". Disponível: {item.quantidade}.'
            )
        return cleaned


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
