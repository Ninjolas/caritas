from django import forms
from django.forms import inlineformset_factory
from .models import EntradaBazar, ItemEntradaBazar, Venda, ItemEstoqueBazar, EmpresaParceira


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
    class Meta:
        model = ItemEntradaBazar
        fields = ['descricao', 'categoria', 'tamanho', 'estado', 'quantidade', 'preco_sugerido']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
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
    class Meta:
        model = Venda
        fields = ['item', 'quantidade', 'preco_unitario', 'data', 'observacao']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ItemEstoqueBazarForm(forms.ModelForm):
    class Meta:
        model = ItemEstoqueBazar
        fields = ['descricao', 'categoria', 'tamanho', 'estado', 'quantidade', 'preco_sugerido']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tamanho': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'preco_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
