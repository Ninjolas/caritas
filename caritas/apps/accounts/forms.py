from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm

from .models import Usuario


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


class CoordenadorCreateForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'paroquia', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'paroquia': 'Paróquia',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_form_control(self)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.perfil = 'coordenador'
        if commit:
            usuario.save()
        return usuario


class VoluntarioCreateForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_form_control(self)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.perfil = 'voluntario'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_form_control(self)
