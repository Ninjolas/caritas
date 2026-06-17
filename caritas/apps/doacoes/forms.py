from django import forms
from django.forms import inlineformset_factory
from .models import Doacao, ItemDoacao


class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['doador', 'data', 'descricao']
        widgets = {
            'doador': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'doador': 'Doador',
            'data': 'Data',
            'descricao': 'Observações',
        }


class ItemDoacaoForm(forms.ModelForm):
    class Meta:
        model = ItemDoacao
        fields = ['nome', 'categoria', 'categoria_outro', 'quantidade', 'unidade', 'data_validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do item'}),
            'categoria': forms.Select(attrs={'class': 'form-select categoria-select'}),
            'categoria_outro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique o tipo'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantidade'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: kg, unidade'}),
            'data_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'data_validade': 'Data de validade',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_outro'].required = False
        self.fields['data_validade'].required = False
        if not kwargs.get('instance'):
            self.initial['quantidade'] = None
            self.initial['unidade'] = ''


ItemDoacaoFormSet = inlineformset_factory(
    Doacao, ItemDoacao,
    form=ItemDoacaoForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True
)
