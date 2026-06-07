from django import forms
from django.forms import inlineformset_factory
from .models import Doacao, ItemDoacao


class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['doador', 'data', 'tipo', 'descricao']
        widgets = {
            'doador': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ItemDoacaoForm(forms.ModelForm):
    class Meta:
        model = ItemDoacao
        fields = ['nome', 'categoria', 'quantidade', 'unidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do item'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: kg, unidade'}),
        }


ItemDoacaoFormSet = inlineformset_factory(
    Doacao, ItemDoacao,
    form=ItemDoacaoForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)
