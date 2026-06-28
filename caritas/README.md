# Sistema Cáritas

Sistema de gestão social desenvolvido em Django para apoiar as atividades da Cáritas Diocesana, com isolamento de dados por paróquia.

**Stack:** Python 3.11, Django 4.2, PostgreSQL 15, Docker + Docker Compose, Bootstrap 5.3

---

## Módulos disponíveis

| Módulo | Descrição |
|--------|-----------|
| **Famílias** | Cadastro de famílias atendidas e seus dependentes |
| **Estoque** | Controle de produtos com catálogo, validade e alertas |
| **Doações** | Registro de doações recebidas (itens e financeiro) |
| **Atendimentos** | Histórico de atendimentos vinculados às famílias |
| **Cestas** | Recebimento de cestas (itens lançados no estoque automaticamente), modelos de cesta para pré-preencher entregas, e listagem separada de cestas recebidas e entregues |
| **Bazar** | Estoque, doações e vendas do bazar de roupas |
| **Brechó** | Eventos de brechó com controle de vendas |
| **Financeiro** | Movimentações de entrada e saída por paróquia/diocese |
| **Relatórios** | Resumos e gráficos por período com navegação mensal, histórico dos últimos 6 meses e exportação em CSV |

---

## Como rodar localmente

```bash
# Subir o ambiente
docker-compose up --build

# Rodar as migrations
docker-compose exec web python manage.py migrate

# Popular com dados de exemplo
docker-compose exec web python manage.py seed

# Acessar
http://localhost:8000
```

---

## Estrutura do projeto

```
caritas/
├── apps/
│   ├── accounts/       # Usuários, perfis e paróquias
│   ├── familias/       # Famílias e dependentes
│   ├── estoque/        # Catálogo e controle de estoque
│   ├── doacoes/        # Doações recebidas
│   ├── atendimentos/   # Atendimentos às famílias
│   ├── cestas/         # Cestas básicas
│   ├── bazar/          # Bazar de roupas
│   ├── brecho/         # Eventos de brechó
│   ├── financeiro/     # Movimentações financeiras
│   └── relatorios/     # Relatórios e gráficos
├── config/             # Configurações (base, development, production)
├── templates/
├── static/
├── build.sh            # Script de build para o Render
└── manage.py
```
