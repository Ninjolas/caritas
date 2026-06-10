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
