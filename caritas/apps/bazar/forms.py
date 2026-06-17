from django import forms
from django.forms import inlineformset_factory
from .models import CategoriaBazar, EntradaBazar, ItemEntradaBazar, Venda, ItemEstoqueBazar, EmpresaParceira


def _categoria_choices():
    """Select com optgroups: categorias raiz e suas subcategorias."""
    choices = [('', '---------')]
    raizes = CategoriaBazar.objects.filter(pai=None, ativa=True).prefetch_related('subcategorias')
    for raiz in raizes:
        subs = raiz.subcategorias.filter(ativa=True)
        if subs.exists():
            grupo = [(sub.pk, sub.nome) for sub in subs]
            choices.append((raiz.nome, grupo))
        else:
            choices.append((raiz.pk, raiz.nome))
    return choices


class CategoriaWidget(forms.Select):
    def optgroups(self, name, value, attrs=None):
        return super().optgroups(name, value, attrs)


class CategoriaBazarForm(forms.ModelForm):
    pai = forms.ModelChoiceField(
        queryset=CategoriaBazar.objects.filter(pai=None, ativa=True),
        required=False,
        empty_label='--- Categoria raiz ---',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoria pai (opcional)',
    )

    class Meta:
        model = CategoriaBazar
        fields = ['nome', 'pai', 'ativa']
        labels = {'nome': 'Nome', 'ativa': 'Ativa'}
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EmpresaParceiraForm(forms.ModelForm):
    class Meta:
        model = EmpresaParceira
        fields = ['nome', 'cnpj', 'contato_nome', 'contato_telefone', 'contato_email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EntradaBazarForm(forms.ModelForm):
    class Meta:
        model = EntradaBazar
        fields = ['tipo_entrada', 'tipo_doador', 'doador_nome', 'doador_contato', 'empresa', 'valor', 'data', 'observacao']
        widgets = {
            'tipo_entrada': forms.Select(attrs={'class': 'form-select'}),
            'tipo_doador': forms.Select(attrs={'class': 'form-select'}),
            'empresa': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doador_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'doador_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ItemEntradaBazarForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=CategoriaBazar.objects.filter(ativa=True),
        required=False,
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoria',
    )

    class Meta:
        model = ItemEntradaBazar
        fields = ['descricao', 'categoria', 'tamanho', 'estado', 'quantidade', 'preco_sugerido']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tamanho': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


ItemEntradaBazarFormSet = inlineformset_factory(
    EntradaBazar, ItemEntradaBazar,
    form=ItemEntradaBazarForm,
    extra=1, min_num=1, validate_min=True, can_delete=True
)


class VendaForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=ItemEstoqueBazar.objects.filter(quantidade__gt=0).select_related('categoria'),
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Item',
    )

    class Meta:
        model = Venda
        fields = ['item', 'quantidade', 'preco_unitario', 'data', 'observacao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned = super().clean()
        item = cleaned.get('item')
        qtd = cleaned.get('quantidade')
        if item and qtd and qtd > item.quantidade:
            raise forms.ValidationError(
                f'Estoque insuficiente para "{item.descricao}". Disponível: {item.quantidade}.'
            )
        return cleaned


class ItemEstoqueBazarForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=CategoriaBazar.objects.filter(ativa=True),
        required=False,
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoria',
    )

    class Meta:
        model = ItemEstoqueBazar
        fields = ['descricao', 'categoria', 'tamanho', 'estado', 'quantidade', 'preco_sugerido']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tamanho': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'preco_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
