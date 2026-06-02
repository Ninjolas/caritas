# Sistema Cáritas

Sistema de gestão social para cadastro e acompanhamento de famílias atendidas.

**Stack:** Python 3.11, Django 4.2, PostgreSQL 15, Docker + Docker Compose, Bootstrap 5.3

## Como rodar

```bash
# Subir o ambiente
docker-compose up --build

# Rodar as migrations
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Acessar
http://localhost:8000
```
