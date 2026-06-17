from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def coordenador_required(view_func):
    def check(user):
        if user.is_authenticated and user.perfil in ['coordenador', 'administrador']:
            return True
        raise PermissionDenied
    return user_passes_test(check, login_url='/login/')(view_func)


def admin_required(view_func):
    def check(user):
        if user.is_authenticated and user.perfil == 'administrador':
            return True
        raise PermissionDenied
    return user_passes_test(check, login_url='/login/')(view_func)


def bazar_required(view_func):
    """Permite acesso a coordenador do bazar, voluntário do bazar e administrador."""
    def check(user):
        if user.is_authenticated and user.perfil in ['coordenador_bazar', 'voluntario_bazar', 'administrador']:
            return True
        raise PermissionDenied
    return user_passes_test(check, login_url='/login/')(view_func)


def coordenador_bazar_required(view_func):
    """Permite acesso apenas a coordenador do bazar e administrador."""
    def check(user):
        if user.is_authenticated and user.perfil in ['coordenador_bazar', 'administrador']:
            return True
        raise PermissionDenied
    return user_passes_test(check, login_url='/login/')(view_func)


def modulo_paroquia_required(view_func):
    """Bloqueia acesso de usuários exclusivos do bazar a módulos da paróquia."""
    def check(user):
        if user.is_authenticated and user.perfil not in ['voluntario_bazar', 'coordenador_bazar']:
            return True
        raise PermissionDenied
    return user_passes_test(check, login_url='/login/')(view_func)
