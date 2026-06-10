from django import forms

from .models import Dependente, Familia


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        exclude = ['id_interno', 'criado_por', 'criado_em', 'paroquia_responsavel']
        widgets = {
            'responsavel_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'possui_cpf': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_possui_cpf'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'escolaridade': forms.Select(attrs={'class': 'form-select'}),
            'ocupacao': forms.TextInput(attrs={'class': 'form-control'}),
            'local_trabalho': forms.TextInput(attrs={'class': 'form-control'}),
            'situacao_vulnerabilidade': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'renda_familiar': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bolsa_familia': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_bolsa_familia'}),
            'valor_beneficio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'qtd_pessoas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'qtd_criancas': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        possui_cpf = cleaned_data.get('possui_cpf')
        cpf = cleaned_data.get('cpf')
        if possui_cpf and not cpf:
            self.add_error('cpf', 'CPF é obrigatório quando o responsável possui CPF.')
        return cleaned_data


class DependenteForm(forms.ModelForm):
    class Meta:
        model = Dependente
        exclude = ['familia']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
        }
