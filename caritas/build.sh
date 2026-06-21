#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Zera todos os dados se RESET_DB=true (remova a variável após o deploy)
if [ "$RESET_DB" = "true" ]; then
    echo ">>> RESET_DB detectado: limpando todos os dados do banco..."
    python manage.py flush --no-input
    echo ">>> Banco zerado."
fi

python manage.py migrate

python manage.py shell << 'EOF'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')

if not password:
    print('DJANGO_SUPERUSER_PASSWORD não definida — pulando criação do admin.')
else:
    user, created = User.objects.get_or_create(username=username)
    user.email    = email
    user.perfil   = 'administrador'
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print(f'Admin "{username}" {"criado" if created else "atualizado"} com sucesso.')
EOF
