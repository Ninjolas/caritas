# Prompt — Geração do Projeto Django Cáritas (Incremento 3)

Preciso que você gere um projeto Django completo chamado **caritas** para um sistema de gestão social. Siga exatamente as especificações abaixo.

**Stack:** Python 3.11, Django 4.2, PostgreSQL 15, Docker + Docker Compose, Bootstrap 5.3

---

## Estrutura de pastas

```
caritas/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/
│   └── familias/
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   └── login.html
│   └── familias/
│       ├── dashboard.html
│       └── cadastro.html
└── static/
    └── css/
        └── custom.css
```

---

## Docker

**Dockerfile:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**docker-compose.yml** com dois serviços:
- `db`: PostgreSQL 15, banco `caritas_db`, usuário `caritas`, senha `caritas123`
- `web`: Django na porta 8000, depende do `db`, roda `python manage.py runserver 0.0.0.0:8000`

---

## requirements.txt

```
django==4.2.11
psycopg2-binary==2.9.9
python-decouple==3.8
```

---

## Settings

**base.py** com:
- `INSTALLED_APPS` incluindo `apps.accounts` e `apps.familias`
- `AUTH_USER_MODEL = 'accounts.Usuario'`
- `TEMPLATES` apontando para a pasta `templates/`
- `STATIC_URL` e `STATICFILES_DIRS` configurados
- `LOGIN_URL = '/login/'`
- `LOGIN_REDIRECT_URL = '/dashboard/'`

**development.py** importando `base.py` e configurando o banco PostgreSQL via variáveis de ambiente com python-decouple (com fallback para localhost).

---

## App: accounts

**Model `Usuario`** estendendo `AbstractUser` com campos extras:
- `perfil`: CharField com choices `voluntario`, `coordenador`, `administrador`
- `paroquia`: CharField com null=True, blank=True

**Views:**
- Login usando `LoginView` do Django com template `accounts/login.html`
- Logout redirecionando para `/login/`

**URLs:** `/login/` e `/logout/`

---

## App: familias

### Models

**`Familia`** com os campos:

| Campo | Tipo | Obs |
|---|---|---|
| `id_interno` | CharField único | Gerado automaticamente se sem CPF |
| `possui_cpf` | BooleanField | default True |
| `cpf` | CharField | blank=True, null=True |
| `responsavel_nome` | CharField | — |
| `nacionalidade` | CharField | — |
| `endereco` | CharField | — |
| `telefone` | CharField | blank=True |
| `escolaridade` | CharField | choices: fundamental_incompleto, fundamental_completo, medio_incompleto, medio_completo, superior |
| `ocupacao` | CharField | blank=True |
| `local_trabalho` | CharField | blank=True |
| `situacao_vulnerabilidade` | TextField | blank=True |
| `renda_familiar` | DecimalField | — |
| `bolsa_familia` | BooleanField | default False |
| `valor_beneficio` | DecimalField | blank=True, null=True |
| `qtd_pessoas` | IntegerField | — |
| `qtd_criancas` | IntegerField | default 0 |
| `paroquia_responsavel` | CharField | — |
| `criado_por` | ForeignKey → Usuario | null=True |
| `criado_em` | DateTimeField | auto_now_add=True |

No método `save()`, se `possui_cpf` for `False` e `id_interno` estiver vazio, gerar ID no formato:
```
INT-{paroquia_responsavel[:3].upper()}-{uuid4().hex[:8].upper()}
```

**`Dependente`** com os campos:

| Campo | Tipo | Obs |
|---|---|---|
| `familia` | ForeignKey → Familia | on_delete=CASCADE |
| `nome` | CharField | — |
| `idade` | IntegerField | — |
| `genero` | CharField | choices: masculino, feminino, outro |

### Forms

- **`FamiliaForm`** com todos os campos de Familia. Validação: se `possui_cpf` for True, `cpf` é obrigatório.
- **`DependenteForm`** simples com os campos de Dependente.

### Views

- **`dashboard`**: `@login_required`, renderiza `familias/dashboard.html` com contagem de famílias cadastradas
- **`cadastrar_familia`**: `@login_required`, GET exibe o form, POST salva e redireciona para dashboard com mensagem de sucesso. Usar `formset_factory` para dependentes (min=0, max=10, extra=1)

### URLs

`/dashboard/` e `/familias/cadastrar/`

---

## Templates (Bootstrap 5 via CDN)

### base.html
- Navbar com: nome do sistema "Sistema Cáritas", nome do usuário logado e link de logout
- Bloco `{% block content %}`
- Rodapé simples com o nome do sistema
- Bootstrap 5 carregado via CDN

### accounts/login.html
- Card centralizado na tela
- Campos de usuário e senha
- Botão "Entrar"
- Fundo com cor `#EBF5FB`

### familias/dashboard.html
- Saudação: "Bem-vindo, {{ user.get_full_name }}"
- Card exibindo total de famílias cadastradas
- Cards de navegação para os módulos:
  - Cadastrar Família → `/familias/cadastrar/`
  - Atendimentos → (em breve)
  - Estoque → (em breve)
  - Relatórios → (em breve)

### familias/cadastro.html
- Formulário dividido em seções com `<fieldset>`:
  1. **Dados Pessoais** (nome, CPF, possui_cpf, nacionalidade, endereço, telefone)
  2. **Dados Socioeconômicos** (escolaridade, ocupação, local_trabalho, renda_familiar, bolsa_familia, valor_beneficio, situacao_vulnerabilidade)
  3. **Composição Familiar** (qtd_pessoas, qtd_criancas)
  4. **Dependentes** (formset com botão "Adicionar Dependente")
- Campo CPF visível/oculto via JavaScript simples conforme o valor de `possui_cpf`
- Botões: "Salvar" e "Cancelar" (volta ao dashboard)

---

## URLs principal (config/urls.py)

- Incluir URLs de `accounts` e `familias`
- Redirecionar `/` para `/dashboard/`

---

## README.md

Gerar um README com as instruções:

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

---

## Instruções finais

- Gere **todos os arquivos completos e funcionais**
- Nada com `pass` ou `# TODO` — tudo deve estar implementado
- Todos os arquivos `__init__.py` necessários devem ser criados
- Os apps devem ter `apps.py` com `AppConfig` corretamente configurado
