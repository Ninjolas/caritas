from django import forms
from .models import ItemEstoque


class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = ['nome', 'categoria', 'categoria_outro', 'quantidade', 'unidade', 'validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do item'}),
            'categoria': forms.Select(attrs={'class': 'form-select', 'id': 'id_categoria'}),
            'categoria_outro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique o tipo'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantidade'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: kg, unidade, caixa'}),
            'validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do item',
            'categoria': 'Categoria',
            'categoria_outro': 'Especificação',
            'quantidade': 'Quantidade',
            'unidade': 'Unidade (ex: kg, unidade, caixa)',
            'validade': 'Data de validade (opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_outro'].required = False
        if not kwargs.get('instance'):
            self.initial['quantidade'] = None
            self.initial['unidade'] = ''
