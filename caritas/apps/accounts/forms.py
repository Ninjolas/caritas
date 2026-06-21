from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm

from .models import Paroquia, Usuario


class TrocarSenhaForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


def _apply_form_control(form):
    for field in form.fields.values():
        widget = field.widget
        if hasattr(widget, 'input_type') and widget.input_type in ('checkbox',):
            widget.attrs['class'] = 'form-check-input'
        elif hasattr(widget, 'attrs'):
            existing = widget.attrs.get('class', '')
            if 'form-control' not in existing and 'form-select' not in existing:
                widget.attrs['class'] = 'form-control'


class UsuarioCreateForm(UserCreationForm):
    perfil = forms.ChoiceField(
        choices=Usuario.PERFIL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Nível de acesso',
    )
    paroquia = forms.ModelChoiceField(
        queryset=Paroquia.objects.filter(ativa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Paróquia',
        empty_label='---------',
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'perfil', 'paroquia', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def __init__(self, *args, solicitante=None, **kwargs):
        super().__init__(*args, **kwargs)

        if solicitante:
            if solicitante.perfil == 'coordenador':
                self.fields['perfil'].choices = [('voluntario', 'Voluntário')]
                self.fields['paroquia'].widget = forms.HiddenInput()
                if not self.data:
                    self.initial['paroquia'] = solicitante.paroquia
            elif solicitante.perfil == 'coordenador_bazar':
                self.fields['perfil'].choices = [('voluntario_bazar', 'Voluntário do Bazar')]
                self.fields.pop('paroquia', None)

        _apply_form_control(self)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.perfil = self.cleaned_data.get('perfil', 'voluntario')
        usuario.paroquia = self.cleaned_data.get('paroquia')
        if commit:
            usuario.save()
        return usuario


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'is_active']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'is_active': 'Ativo',
        }

    def __init__(self, *args, solicitante=None, **kwargs):
        super().__init__(*args, **kwargs)
        if solicitante and solicitante.perfil == 'administrador':
            self.fields['perfil'] = forms.ChoiceField(
                choices=Usuario.PERFIL_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                label='Nível de acesso',
                initial=self.instance.perfil if self.instance else 'voluntario',
            )
            self.fields['paroquia'] = forms.ModelChoiceField(
                queryset=Paroquia.objects.filter(ativa=True),
                required=False,
                widget=forms.Select(attrs={'class': 'form-select'}),
                label='Paróquia',
                empty_label='---------',
                initial=self.instance.paroquia if self.instance else None,
            )
        _apply_form_control(self)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if 'perfil' in self.cleaned_data:
            usuario.perfil = self.cleaned_data['perfil']
        if 'paroquia' in self.cleaned_data:
            usuario.paroquia = self.cleaned_data.get('paroquia')
        if commit:
            usuario.save()
        return usuario


class ParoquiaForm(forms.ModelForm):
    class Meta:
        model = Paroquia
        fields = ['nome', 'cidade', 'bairro', 'endereco', 'telefone', 'email', 'ativa']
        labels = {
            'nome': 'Nome da Paróquia',
            'cidade': 'Cidade',
            'bairro': 'Bairro (opcional)',
            'endereco': 'Endereço (opcional)',
            'telefone': 'Telefone (opcional)',
            'email': 'E-mail (opcional)',
            'ativa': 'Ativa',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, número'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
