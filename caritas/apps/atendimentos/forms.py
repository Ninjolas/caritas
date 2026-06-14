from django import forms
from .models import Atendimento
from apps.familias.models import Familia


class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['familia', 'tipo', 'data', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'familia': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, paroquia=None, **kwargs):
        super().__init__(*args, **kwargs)
        if paroquia:
            self.fields['familia'].queryset = Familia.objects.filter(
                paroquia_responsavel=paroquia
            ).order_by('responsavel_nome')
