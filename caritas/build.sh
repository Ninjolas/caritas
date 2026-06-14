#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Cria superusuário apenas se não existir (usa variáveis de ambiente do Render)
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
import os
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'),
        perfil='administrador',
    )
    print(f'Superusuário {username} criado.')
else:
    print(f'Superusuário {username} já existe.')
"
