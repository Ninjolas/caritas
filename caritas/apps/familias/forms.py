from django import forms

from .models import Dependente, Familia


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = [
            'possui_cpf', 'cpf', 'responsavel_nome', 'nome_mae', 'nome_pai',
            'data_nascimento', 'nacionalidade', 'endereco', 'telefone',
            'escolaridade', 'ocupacao', 'local_trabalho', 'situacao_vulnerabilidade',
            'renda_familiar', 'bolsa_familia', 'valor_beneficio',
            'qtd_pessoas', 'qtd_criancas',
            'data_ultima_visita', 'data_ultimo_atendimento',
        ]
        widgets = {
            'possui_cpf': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_possui_cpf'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'responsavel_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_pai': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
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
            'data_ultima_visita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_ultimo_atendimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        possui_cpf = cleaned_data.get('possui_cpf')
        cpf = cleaned_data.get('cpf')
        if possui_cpf and not cpf:
            self.add_error('cpf', 'CPF é obrigatório quando marcado como "possui CPF".')
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
