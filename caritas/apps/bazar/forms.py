from django import forms
from django.forms import inlineformset_factory
from .models import CatalogoBazar, EntradaBazar, ItemEntradaBazar, Venda, ItemEstoqueBazar, EmpresaParceira


class CatalogoBazarForm(forms.ModelForm):
    class Meta:
        model = CatalogoBazar
        fields = ['nome', 'genero', 'ativo']
        labels = {'nome': 'Tipo de roupa', 'genero': 'Gênero', 'ativo': 'Ativo'}
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
    catalogo = forms.ModelChoiceField(
        queryset=CatalogoBazar.objects.filter(ativo=True),
        required=False,
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Catálogo',
    )

    class Meta:
        model = ItemEntradaBazar
        fields = ['descricao', 'catalogo', 'tamanho', 'estado', 'quantidade', 'preco_sugerido']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'tamanho': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].required = False


ItemEntradaBazarFormSet = inlineformset_factory(
    EntradaBazar, ItemEntradaBazar,
    form=ItemEntradaBazarForm,
    extra=1, min_num=1, validate_min=True, can_delete=True
)


class VendaForm(forms.ModelForm):
    catalogo_filtro = forms.ModelChoiceField(
        queryset=CatalogoBazar.objects.filter(ativo=True),
        required=False,
        empty_label='--- Todos os catálogos ---',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_catalogo_filtro'}),
        label='Catálogo',
    )
    item = forms.ModelChoiceField(
        queryset=ItemEstoqueBazar.objects.filter(quantidade__gt=0).select_related('catalogo'),
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_item'}),
        label='Item',
    )

    class Meta:
        model = Venda
        fields = ['catalogo_filtro', 'item', 'quantidade', 'preco_unitario', 'data', 'observacao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def _label(obj):
            partes = [str(obj.catalogo) if obj.catalogo else '—', obj.get_tamanho_display(), obj.get_estado_display()]
            if obj.descricao:
                partes.append(obj.descricao)
            return f"{' — '.join(partes)} ({obj.quantidade} un.)"

        self.fields['item'].label_from_instance = _label

    def clean(self):
        cleaned = super().clean()
        item = cleaned.get('item')
        qtd = cleaned.get('quantidade')
        if item and qtd and qtd > item.quantidade:
            nome = str(item.catalogo) if item.catalogo else item.descricao or 'item'
            raise forms.ValidationError(
                f'Estoque insuficiente para "{nome}". Disponível: {item.quantidade}.'
            )
        return cleaned


class ItemEstoqueBazarForm(forms.ModelForm):
    catalogo = forms.ModelChoiceField(
        queryset=CatalogoBazar.objects.filter(ativo=True),
        required=False,
        empty_label='--- Selecione ---',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Catálogo',
    )

    class Meta:
        model = ItemEstoqueBazar
        fields = ['descricao', 'catalogo', 'tamanho', 'estado', 'quantidade', 'preco_sugerido']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'tamanho': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'preco_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
