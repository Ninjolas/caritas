import json

from django import forms
from django.forms import inlineformset_factory

from apps.estoque.models import ProdutoCatalogo
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
    produto = forms.ModelChoiceField(
        queryset=ProdutoCatalogo.objects.filter(ativo=True).order_by('categoria', 'nome'),
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select produto-select'}),
        label='Produto',
    )

    class Meta:
        model = ItemDoacao
        fields = ['produto', 'quantidade', 'unidade', 'data_validade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Qtd'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control unidade-input', 'placeholder': 'ex: kg, unidade'}),
            'data_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control campo-validade'}),
        }
        labels = {
            'data_validade': 'Validade',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_validade'].required = False
        if not kwargs.get('instance'):
            self.initial['quantidade'] = None
            self.initial['unidade'] = ''


def get_produtos_json():
    data = {}
    for p in ProdutoCatalogo.objects.filter(ativo=True):
        data[str(p.pk)] = {
            'unidade': p.unidade_padrao,
            'categoria': p.get_categoria_display(),
            'categoria_key': p.categoria,
        }
    return json.dumps(data)


ItemDoacaoFormSet = inlineformset_factory(
    Doacao, ItemDoacao,
    form=ItemDoacaoForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True
)
