from django import forms
from .models import BrechoEvento, VendaBrecho
from apps.estoque.models import ItemEstoque


class BrechoEventoForm(forms.ModelForm):
    class Meta:
        model = BrechoEvento
        fields = ['nome', 'data', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class VendaBrechoForm(forms.ModelForm):
    class Meta:
        model = VendaBrecho
        fields = ['item_estoque', 'quantidade', 'preco_unitario']
        widgets = {
            'item_estoque': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            self.fields['item_estoque'].queryset = ItemEstoque.objects.filter(
                paroquia=paroquia,
                categoria='roupa',
                quantidade__gt=0,
            )
