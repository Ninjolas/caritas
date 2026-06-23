# Sistema de Gestão Cáritas

Sistema web desenvolvido em Django para apoiar as atividades da Cáritas Diocesana, cobrindo controle de estoque, doações, atendimentos a famílias, cestas básicas, bazar, brechó e financeiro — com isolamento de dados por paróquia.

---

## Acesso ao sistema

**URL de produção:** https://caritas-sistema.onrender.com

> O serviço está hospedado no plano gratuito do Render. Na primeira requisição após inatividade pode levar até 30 segundos para iniciar.

---

## Módulos disponíveis

| Módulo | Descrição |
|--------|-----------|
| **Famílias** | Cadastro de famílias atendidas e seus dependentes |
| **Estoque** | Controle de produtos com catálogo, validade e alertas |
| **Doações** | Registro de doações recebidas (itens e financeiro) |
| **Atendimentos** | Histórico de atendimentos vinculados às famílias |
| **Cestas** | Montagem e entrega de cestas básicas |
| **Bazar** | Estoque, doações e vendas do bazar de roupas |
| **Brechó** | Eventos de brechó com controle de vendas |
| **Financeiro** | Movimentações de entrada e saída por paróquia/diocese |
| **Relatórios** | Gráficos e resumos por período |

---

## Rodando localmente

**Pré-requisitos:** Python 3.11+, pip

```bash
cd caritas
pip install -r requirements.txt

export DJANGO_SETTINGS_MODULE=config.settings.development

python manage.py migrate
python manage.py seed          # popula com dados de exemplo
python manage.py runserver
```

---

## Resetar e re-popular o banco (Render)

1. No painel do Render, adicione a variável de ambiente: `RESET_DB = true`
2. Dispare um novo deploy (qualquer push ou deploy manual)
3. O `build.sh` irá: **flush → migrate → seed**
4. Após o deploy, **remova ou desative** a variável `RESET_DB` para não resetar nos próximos deploys

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