# Prompt — Deploy no Render

Configurar o projeto Django Cáritas para publicação no Render (plano gratuito). O objetivo é ter o sistema acessível via link público para a homologação com o cliente.

---

## 1. Adicionar dependências de produção em `requirements.txt`

Adicionar (se ainda não existirem) os seguintes pacotes:

```
gunicorn==21.2.0
dj-database-url==2.1.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
python-decouple==3.8
```

---

## 2. Criar `config/settings/production.py`

```python
from .base import *
import dj_database_url
from decouple import config

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Banco de dados via DATABASE_URL (fornecido automaticamente pelo Render)
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        conn_max_age=600,
        ssl_require=True,
    )
}

# Arquivos estáticos com WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Segurança
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

## 3. Atualizar `config/settings/base.py`

Verificar se `BASE_DIR` está definido com `pathlib.Path`:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

Verificar se `STATIC_URL` está definido:

```python
STATIC_URL = '/static/'
```

---

## 4. Atualizar `config/wsgi.py`

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
```

---

## 5. Criar `build.sh` na raiz do projeto

Este script é executado pelo Render a cada deploy:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Tornar executável:

```bash
chmod +x build.sh
```

---

## 6. Criar `render.yaml` na raiz do projeto

```yaml
services:
  - type: web
    name: caritas-sistema
    env: python
    region: oregon
    plan: free
    buildCommand: "./build.sh"
    startCommand: "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings.production
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
      - key: DATABASE_URL
        fromDatabase:
          name: caritas-db
          property: connectionString
      - key: PYTHON_VERSION
        value: "3.11.0"

databases:
  - name: caritas-db
    databaseName: caritas
    user: caritas_user
    plan: free
```

---

## 7. Criar `.env.example` na raiz do projeto

Arquivo de referência para variáveis necessárias (não commitar o `.env` real):

```
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=.onrender.com,localhost
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
```

---

## 8. Atualizar `.gitignore`

Garantir que os seguintes arquivos estão ignorados:

```
.env
*.pyc
__pycache__/
staticfiles/
db.sqlite3
```

---

## 9. Verificar `config/urls.py`

Adicionar serving de arquivos estáticos em desenvolvimento (o WhiteNoise cuida da produção):

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('familias/', include('apps.familias.urls')),
    path('estoque/', include('apps.estoque.urls')),
    path('doacoes/', include('apps.doacoes.urls')),
    path('atendimentos/', include('apps.atendimentos.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
    path('cestas/', include('apps.cestas.urls')),
    path('brecho/', include('apps.brecho.urls')),
    path('bazar/', include('apps.bazar.urls')),
    path('financeiro/', include('apps.financeiro.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 10. Commit e push para o GitHub

```bash
git add .
git commit -m "chore: configuração para deploy no Render"
git push origin main
```

---

## 11. Instruções para conectar ao Render (fazer manualmente no site)

Após o push, acessar [render.com](https://render.com) e:

1. Criar conta gratuita (não precisa de cartão)
2. Clicar em **New → Blueprint**
3. Conectar o repositório GitHub do projeto
4. O Render vai detectar o `render.yaml` automaticamente
5. Confirmar a criação dos serviços (web + banco)
6. Aguardar o build (primeira vez leva ~3 minutos)
7. O link público estará disponível no formato: `https://caritas-sistema.onrender.com`

---

## Instruções finais

- Todos os arquivos devem ser criados na raiz do projeto (mesmo nível que `manage.py`)
- O `render.yaml` define tanto o serviço web quanto o banco PostgreSQL — ambos gratuitos
- O `build.sh` roda `migrate` automaticamente a cada deploy, então novas migrations são aplicadas sem intervenção manual
- O serviço gratuito do Render hiberna após 15 minutos sem acesso — avisar ao cliente para aguardar alguns segundos na primeira abertura
- Após o primeiro deploy, criar o superusuário via Render Shell: `python manage.py createsuperuser`
