from django import forms
from django.forms import formset_factory, BaseFormSet
from .models import Atendimento
from apps.familias.models import Familia
from apps.estoque.models import ItemEstoque


class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['familia', 'tipo', 'data', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo'}),
            'familia': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            self.fields['familia'].queryset = Familia.objects.filter(
                paroquia_responsavel=paroquia
            ).order_by('responsavel_nome')


class ItemAtendimentoForm(forms.Form):
    item_estoque = forms.ModelChoiceField(
        queryset=ItemEstoque.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select item-estoque-select'}),
        label='Item do estoque',
        empty_label='--- Selecione ---',
    )
    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Qtd'}),
        label='Quantidade',
    )

    def __init__(self, *args, paroquia=None, categoria=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = ItemEstoque.objects.filter(paroquia=paroquia, quantidade__gt=0) if paroquia else ItemEstoque.objects.none()
        if categoria:
            if isinstance(categoria, list):
                qs = qs.filter(categoria__in=categoria)
            else:
                qs = qs.filter(categoria=categoria)
        self.fields['item_estoque'].queryset = qs.order_by('nome', 'validade')

        def _label(obj):
            label = obj.nome
            if obj.validade:
                label += f' — vence {obj.validade.strftime("%d/%m/%Y")}'
            label += f' ({obj.quantidade} {obj.unidade})'
            return label

        self.fields['item_estoque'].label_from_instance = _label


class _BaseItemAtendimentoFormSet(BaseFormSet):
    def __init__(self, *args, paroquia=None, categoria=None, **kwargs):
        self.paroquia = paroquia
        self.categoria = categoria
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['paroquia'] = self.paroquia
        kwargs['categoria'] = self.categoria
        return super()._construct_form(i, **kwargs)


ItemAtendimentoFormSet = formset_factory(
    ItemAtendimentoForm,
    formset=_BaseItemAtendimentoFormSet,
    extra=1,
    min_num=1,
    validate_min=False,
    can_delete=True,
)
