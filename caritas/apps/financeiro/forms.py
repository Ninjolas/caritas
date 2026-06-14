from django import forms
from .models import MovimentacaoFinanceira


class MovimentacaoFinanceiraForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoFinanceira
        fields = ['tipo', 'valor', 'data', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
