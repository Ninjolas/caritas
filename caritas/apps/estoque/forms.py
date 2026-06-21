import json
from django import forms
from .models import ItemEstoque, ProdutoCatalogo


class ProdutoCatalogoForm(forms.ModelForm):
    class Meta:
        model = ProdutoCatalogo
        fields = ['nome', 'categoria', 'unidade_padrao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Arroz, Feijão, Camisa...'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'unidade_padrao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: kg, unidade, caixa'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome do produto',
            'categoria': 'Categoria',
            'unidade_padrao': 'Unidade padrão',
            'ativo': 'Ativo no catálogo',
        }


class ItemEstoqueForm(forms.ModelForm):
    """Formulário para nova entrada de estoque — exige seleção do catálogo."""

    class Meta:
        model = ItemEstoque
        fields = ['produto', 'quantidade', 'unidade', 'validade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select', 'id': 'id_produto'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: kg, unidade, caixa'}),
            'validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'produto': 'Produto',
            'quantidade': 'Quantidade',
            'unidade': 'Unidade',
            'validade': 'Data de validade (opcional)',
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = ProdutoCatalogo.objects.filter(ativo=True)
        if paroquia:
            qs = qs.filter(paroquia=paroquia)
        self.fields['produto'].queryset = qs
        self.fields['produto'].empty_label = 'Selecione um produto do catálogo...'
        self.fields['validade'].required = False
        self.fields['produto'].required = True
        self._paroquia = paroquia

    def get_produtos_json(self):
        qs = ProdutoCatalogo.objects.filter(ativo=True)
        if self._paroquia:
            qs = qs.filter(paroquia=self._paroquia)
        data = {
            p.id: {'unidade': p.unidade_padrao, 'categoria': p.get_categoria_display()}
            for p in qs
        }
        return json.dumps(data)


class ItemEstoqueEditarForm(forms.ModelForm):
    """Formulário de edição — apenas campos mutáveis."""

    class Meta:
        model = ItemEstoque
        fields = ['quantidade', 'unidade', 'validade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'unidade': forms.TextInput(attrs={'class': 'form-control'}),
            'validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'quantidade': 'Quantidade',
            'unidade': 'Unidade',
            'validade': 'Data de validade (opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['validade'].required = False
