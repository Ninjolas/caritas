from django import forms
from .models import ItemEstoque


class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = ['nome', 'categoria', 'quantidade', 'unidade', 'validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do item'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: kg, unidade, caixa'}),
            'validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do item',
            'categoria': 'Categoria',
            'quantidade': 'Quantidade',
            'unidade': 'Unidade (ex: kg, unidade, caixa)',
            'validade': 'Data de validade (opcional)',
        }
