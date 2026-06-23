import json
from django import forms
from django.forms import formset_factory, BaseFormSet, inlineformset_factory
from .models import (
    CestaRecebida, ItemCestaRecebida,
    CestaEntregue, ItemCestaEntregue,
    ModeloCesta, ModeloItemCesta,
)
from apps.estoque.models import ItemEstoque
from apps.familias.models import Familia


UNIDADE_CHOICES = [
    ('kg', 'kg'),
    ('g', 'g'),
    ('litro', 'litro'),
    ('unidade', 'unidade'),
    ('pacote', 'pacote'),
    ('lata', 'lata'),
    ('caixa', 'caixa'),
]


# ── Cesta Recebida ─────────────────────────────────────────────────────────────

class CestaRecebidaForm(forms.ModelForm):
    class Meta:
        model = CestaRecebida
        fields = ['data', 'doador_nome', 'observacao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doador_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do doador (opcional)'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ItemCestaRecebidaForm(forms.Form):
    nome = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Arroz'}),
        label='Item',
    )
    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        label='Qtd',
    )
    unidade = forms.ChoiceField(
        choices=UNIDADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Unidade',
    )
    validade = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Validade',
    )


ItemCestaRecebidaFormSet = formset_factory(
    ItemCestaRecebidaForm,
    extra=1, min_num=1, validate_min=True, can_delete=True,
)


# ── Cesta Entregue ─────────────────────────────────────────────────────────────

class ItemCestaEntregueForm(forms.Form):
    item_estoque = forms.ModelChoiceField(
        queryset=ItemEstoque.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select item-estoque-select'}),
        label='Item do estoque',
        empty_label='--- Selecione ---',
    )
    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control quantidade-input', 'min': 1}),
        label='Qtd',
    )

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = (
            ItemEstoque.objects
            .filter(paroquia=paroquia, quantidade__gt=0, categoria='alimento')
            .order_by('nome', 'validade')
        ) if paroquia else ItemEstoque.objects.none()
        self.fields['item_estoque'].queryset = qs
        stocks = {str(i.pk): {'qtd': i.quantidade, 'unidade': i.unidade} for i in qs}
        self.fields['item_estoque'].widget.attrs['data-stocks'] = json.dumps(stocks)

        def _label(obj):
            label = obj.nome
            if obj.validade:
                label += f' — vence {obj.validade.strftime("%d/%m/%Y")}'
            label += f' ({obj.quantidade} {obj.unidade})'
            return label

        self.fields['item_estoque'].label_from_instance = _label

    def clean(self):
        cleaned = super().clean()
        item = cleaned.get('item_estoque')
        qtd = cleaned.get('quantidade')
        if item and qtd and qtd > item.quantidade:
            raise forms.ValidationError(
                f'Estoque insuficiente para "{item.nome}". Disponível: {item.quantidade}.'
            )
        return cleaned


class _BaseItemCestaEntregueFormSet(BaseFormSet):
    def __init__(self, *args, paroquia=None, **kwargs):
        self.paroquia = paroquia
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['paroquia'] = self.paroquia
        return super()._construct_form(i, **kwargs)


ItemCestaEntregueFormSet = formset_factory(
    ItemCestaEntregueForm,
    formset=_BaseItemCestaEntregueFormSet,
    extra=1, min_num=1, validate_min=True, can_delete=True,
)


class CestaEntregueEditarForm(forms.ModelForm):
    class Meta:
        model = CestaEntregue
        fields = ['data', 'observacao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CestaEntregueForm(forms.ModelForm):
    class Meta:
        model = CestaEntregue
        fields = ['familia', 'data', 'modelo_usado', 'observacao']
        widgets = {
            'familia': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'modelo_usado': forms.Select(attrs={'class': 'form-select', 'id': 'id_modelo_usado'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {'modelo_usado': 'Modelo de cesta (opcional)'}

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            self.fields['familia'].queryset = Familia.objects.filter(
                paroquia_responsavel=paroquia
            ).order_by('responsavel_nome')
        self.fields['modelo_usado'].queryset = ModeloCesta.objects.all().order_by('nome')
        self.fields['modelo_usado'].required = False
        self.fields['modelo_usado'].empty_label = '--- Sem modelo ---'


# ── Modelo de Cesta ────────────────────────────────────────────────────────────

class ModeloCestaForm(forms.ModelForm):
    class Meta:
        model = ModeloCesta
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }


ModeloItemCestaInlineFormSet = inlineformset_factory(
    ModeloCesta, ModeloItemCesta,
    fields=['nome', 'quantidade', 'unidade'],
    widgets={
        'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Arroz'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: kg'}),
    },
    extra=1, min_num=1, validate_min=True, can_delete=True,
)
