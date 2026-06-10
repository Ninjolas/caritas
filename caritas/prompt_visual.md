# Prompt — Refatoração Visual dos Templates Django (Bootstrap 5)

Refatorar todos os templates HTML do projeto Cáritas para um visual profissional usando Bootstrap 5 (já instalado via CDN). Não instalar nenhuma dependência nova. Manter toda a lógica Django existente — apenas melhorar o HTML/CSS.

---

## Paleta de cores

Usar as seguintes variáveis CSS no `base.html`:

```css
:root {
    --caritas-primary: #1a5276;    /* azul escuro — cor principal */
    --caritas-secondary: #2e86c1;  /* azul médio — hover, links */
    --caritas-accent: #28b463;     /* verde — ações positivas */
    --caritas-light: #eaf4fb;      /* azul claro — fundos suaves */
    --sidebar-bg: #1a2d3d;         /* sidebar escura */
    --sidebar-text: #cdd8e0;       /* texto claro na sidebar */
    --sidebar-active: #2e86c1;     /* item ativo na sidebar */
}
```

---

## 1. Refatorar `templates/base.html`

Estrutura de layout com sidebar lateral fixa + área de conteúdo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema Cáritas{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            --caritas-primary: #1a5276;
            --caritas-secondary: #2e86c1;
            --caritas-accent: #28b463;
            --caritas-light: #eaf4fb;
            --sidebar-bg: #1a2d3d;
            --sidebar-text: #cdd8e0;
            --sidebar-active: #2e86c1;
        }
        body { background-color: #f0f4f8; }

        /* Sidebar */
        #sidebar {
            width: 240px;
            min-height: 100vh;
            background-color: var(--sidebar-bg);
            position: fixed;
            top: 0; left: 0;
            z-index: 100;
            display: flex;
            flex-direction: column;
        }
        #sidebar .sidebar-brand {
            padding: 1.5rem 1.25rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        #sidebar .sidebar-brand h6 {
            color: #fff;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin: 0;
        }
        #sidebar .sidebar-brand small {
            color: var(--sidebar-text);
            font-size: 11px;
        }
        #sidebar .nav-section {
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.35);
            padding: 1.25rem 1.25rem 0.4rem;
        }
        #sidebar .nav-link {
            color: var(--sidebar-text);
            padding: 0.55rem 1.25rem;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-radius: 0;
            transition: background 0.15s;
        }
        #sidebar .nav-link:hover {
            background-color: rgba(255,255,255,0.07);
            color: #fff;
        }
        #sidebar .nav-link.active {
            background-color: var(--sidebar-active);
            color: #fff;
        }
        #sidebar .nav-link.disabled {
            color: rgba(255,255,255,0.25);
            pointer-events: none;
        }
        #sidebar .nav-link i { font-size: 16px; width: 18px; }
        #sidebar .sidebar-user {
            margin-top: auto;
            padding: 1rem 1.25rem;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        #sidebar .sidebar-user .user-name {
            font-size: 13px;
            font-weight: 500;
            color: #fff;
        }
        #sidebar .sidebar-user .user-role {
            font-size: 11px;
            color: var(--sidebar-text);
            text-transform: capitalize;
        }

        /* Main content */
        #main-content {
            margin-left: 240px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .topbar {
            background: #fff;
            border-bottom: 1px solid #e2e8f0;
            padding: 0.75rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .topbar .page-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--caritas-primary);
            margin: 0;
        }
        .topbar .breadcrumb {
            margin: 0;
            font-size: 13px;
        }
        .page-content {
            padding: 1.5rem;
            flex: 1;
        }

        /* Cards */
        .card { border: 1px solid #e2e8f0; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
        .card-header { background-color: #fff; border-bottom: 1px solid #e2e8f0; font-weight: 600; font-size: 14px; }

        /* Metric cards */
        .metric-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1.25rem;
        }
        .metric-card .metric-icon {
            width: 44px; height: 44px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px;
        }
        .metric-card .metric-value { font-size: 28px; font-weight: 700; color: var(--caritas-primary); }
        .metric-card .metric-label { font-size: 13px; color: #6b7280; }

        /* Badges de perfil */
        .badge-voluntario { background-color: #dbeafe; color: #1d4ed8; }
        .badge-coordenador { background-color: #dcfce7; color: #166534; }
        .badge-administrador { background-color: #fef3c7; color: #92400e; }

        /* Tables */
        .table th { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; border-bottom: 2px solid #e2e8f0; }
        .table td { font-size: 14px; vertical-align: middle; }

        /* Forms */
        .form-label { font-size: 13px; font-weight: 500; color: #374151; }
        .form-control, .form-select { font-size: 14px; border-color: #d1d5db; }
        .form-control:focus, .form-select:focus { border-color: var(--caritas-secondary); box-shadow: 0 0 0 3px rgba(46,134,193,0.15); }
        fieldset.form-section { background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; }
        fieldset.form-section legend { font-size: 13px; font-weight: 600; color: var(--caritas-primary); padding: 0 8px; width: auto; }

        /* Alerts */
        .alert { font-size: 14px; border-radius: 8px; }
    </style>
</head>
<body>

{% if user.is_authenticated %}
<!-- Sidebar -->
<div id="sidebar">
    <div class="sidebar-brand">
        <h6><i class="bi bi-heart-fill me-2" style="color:#e74c3c"></i>Sistema Cáritas</h6>
        <small>{{ user.paroquia|default:"Administração" }}</small>
    </div>

    <nav class="mt-2">
        <span class="nav-section">Principal</span>
        <a href="{% url 'familias:dashboard' %}" class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a href="{% url 'familias:cadastrar' %}" class="nav-link {% if 'familias' in request.path %}active{% endif %}">
            <i class="bi bi-people"></i> Famílias
        </a>

        <span class="nav-section">Operações</span>
        <a href="{% url 'estoque:listagem' %}" class="nav-link {% if 'estoque' in request.path %}active{% endif %}">
            <i class="bi bi-box-seam"></i> Estoque
        </a>
        <a href="{% url 'doacoes:listagem' %}" class="nav-link {% if 'doacoes' in request.path %}active{% endif %}">
            <i class="bi bi-gift"></i> Doações
        </a>
        <a href="#" class="nav-link disabled">
            <i class="bi bi-calendar-check"></i> Atendimentos <span class="badge bg-secondary ms-auto" style="font-size:10px">Em breve</span>
        </a>

        {% if user.perfil == 'coordenador' or user.perfil == 'administrador' %}
        <span class="nav-section">Gestão</span>
        <a href="{% url 'estoque:entrada' %}" class="nav-link">
            <i class="bi bi-plus-circle"></i> Entrada no estoque
        </a>
        <a href="#" class="nav-link disabled">
            <i class="bi bi-graph-up"></i> Relatórios <span class="badge bg-secondary ms-auto" style="font-size:10px">Em breve</span>
        </a>
        <a href="{% url 'accounts:gerenciar_voluntarios' %}" class="nav-link {% if 'voluntarios' in request.path %}active{% endif %}">
            <i class="bi bi-person-badge"></i> Voluntários
        </a>
        {% endif %}

        {% if user.perfil == 'administrador' %}
        <a href="{% url 'accounts:gerenciar_coordenadores' %}" class="nav-link {% if 'coordenadores' in request.path %}active{% endif %}">
            <i class="bi bi-shield-check"></i> Coordenadores
        </a>
        {% endif %}
    </nav>

    <div class="sidebar-user">
        <div class="d-flex align-items-center gap-2">
            <div style="width:32px;height:32px;border-radius:50%;background:var(--sidebar-active);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;color:#fff;">
                {{ user.first_name|first|upper }}{{ user.last_name|first|upper }}
            </div>
            <div>
                <div class="user-name">{{ user.get_full_name|default:user.username }}</div>
                <div class="user-role">{{ user.get_perfil_display }}</div>
            </div>
        </div>
        <a href="{% url 'accounts:logout' %}" class="btn btn-sm w-100 mt-2" style="background:rgba(255,255,255,0.08);color:var(--sidebar-text);font-size:12px;">
            <i class="bi bi-box-arrow-right me-1"></i> Sair
        </a>
    </div>
</div>

<!-- Main -->
<div id="main-content">
    <div class="topbar">
        <div>
            <h1 class="page-title">{% block page_title %}{% endblock %}</h1>
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">{% block breadcrumb %}<li class="breadcrumb-item active">Início</li>{% endblock %}</ol>
            </nav>
        </div>
        <div class="d-flex align-items-center gap-3">
            <span class="badge {% if user.perfil == 'voluntario' %}badge-voluntario{% elif user.perfil == 'coordenador' %}badge-coordenador{% else %}badge-administrador{% endif %} px-3 py-2">
                {{ user.get_perfil_display }}
            </span>
        </div>
    </div>

    <div class="page-content">
        {% if messages %}
            {% for message in messages %}
            <div class="alert alert-{% if message.tags == 'error' %}danger{% else %}{{ message.tags }}{% endif %} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>
</div>

{% else %}
{% block content %}{% endblock %}
{% endif %}

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_js %}{% endblock %}
</body>
</html>
```

> O model `Usuario` precisa ter o método `get_perfil_display` retornando o label legível do perfil. Verificar se o campo `perfil` usa `choices` no model — se sim, Django já gera esse método automaticamente.

---

## 2. Refatorar `templates/familias/dashboard.html`

```html
{% extends 'base.html' %}
{% block title %}Dashboard — Sistema Cáritas{% endblock %}
{% block page_title %}Dashboard{% endblock %}
{% block breadcrumb %}<li class="breadcrumb-item active">Dashboard</li>{% endblock %}

{% block content %}
<p class="text-muted mb-4" style="font-size:15px">
    Bem-vindo, <strong>{{ user.get_full_name|default:user.username }}</strong>.
    {% if user.paroquia %}Paróquia: <strong>{{ user.paroquia }}</strong>.{% endif %}
</p>

<!-- Metric cards -->
<div class="row g-3 mb-4">
    <div class="col-sm-6 col-lg-4">
        <div class="metric-card">
            <div class="d-flex align-items-center gap-3 mb-2">
                <div class="metric-icon" style="background:#eaf4fb;color:#1a5276">
                    <i class="bi bi-people-fill"></i>
                </div>
                <div>
                    <div class="metric-value">{{ total_familias }}</div>
                    <div class="metric-label">Famílias cadastradas</div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-4">
        <div class="metric-card">
            <div class="d-flex align-items-center gap-3 mb-2">
                <div class="metric-icon" style="background:#f0fff4;color:#166534">
                    <i class="bi bi-box-seam-fill"></i>
                </div>
                <div>
                    <div class="metric-value">{{ total_estoque }}</div>
                    <div class="metric-label">Itens em estoque</div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-sm-6 col-lg-4">
        <div class="metric-card">
            <div class="d-flex align-items-center gap-3 mb-2">
                <div class="metric-icon" style="background:#fef3c7;color:#92400e">
                    <i class="bi bi-gift-fill"></i>
                </div>
                <div>
                    <div class="metric-value">{{ total_doacoes_mes }}</div>
                    <div class="metric-label">Doações este mês</div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Atalhos -->
<h6 class="text-muted mb-3" style="font-size:12px;text-transform:uppercase;letter-spacing:1px">Acesso rápido</h6>
<div class="row g-3">
    <div class="col-sm-6 col-lg-3">
        <a href="{% url 'familias:cadastrar' %}" class="card text-decoration-none p-3 d-flex flex-row align-items-center gap-3 hover-shadow">
            <div style="width:44px;height:44px;border-radius:10px;background:#eaf4fb;display:flex;align-items:center;justify-content:center;font-size:20px;color:#1a5276">
                <i class="bi bi-person-plus"></i>
            </div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#1a5276">Cadastrar família</div>
                <div style="font-size:12px;color:#6b7280">Nova família</div>
            </div>
        </a>
    </div>
    <div class="col-sm-6 col-lg-3">
        <a href="{% url 'doacoes:registrar' %}" class="card text-decoration-none p-3 d-flex flex-row align-items-center gap-3">
            <div style="width:44px;height:44px;border-radius:10px;background:#f0fff4;display:flex;align-items:center;justify-content:center;font-size:20px;color:#166534">
                <i class="bi bi-gift"></i>
            </div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#166534">Registrar doação</div>
                <div style="font-size:12px;color:#6b7280">Entrada ou saída</div>
            </div>
        </a>
    </div>
    <div class="col-sm-6 col-lg-3">
        <a href="{% url 'estoque:listagem' %}" class="card text-decoration-none p-3 d-flex flex-row align-items-center gap-3">
            <div style="width:44px;height:44px;border-radius:10px;background:#fef3c7;display:flex;align-items:center;justify-content:center;font-size:20px;color:#92400e">
                <i class="bi bi-box-seam"></i>
            </div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#92400e">Ver estoque</div>
                <div style="font-size:12px;color:#6b7280">Itens disponíveis</div>
            </div>
        </a>
    </div>
    <div class="col-sm-6 col-lg-3">
        <div class="card p-3 d-flex flex-row align-items-center gap-3" style="opacity:0.5;cursor:not-allowed">
            <div style="width:44px;height:44px;border-radius:10px;background:#f3f4f6;display:flex;align-items:center;justify-content:center;font-size:20px;color:#6b7280">
                <i class="bi bi-calendar-check"></i>
            </div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#6b7280">Atendimentos</div>
                <div style="font-size:12px;color:#6b7280">Em breve</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 3. Refatorar `templates/accounts/login.html`

```html
{% extends 'base.html' %}
{% block title %}Entrar — Sistema Cáritas{% endblock %}

{% block content %}
<div style="min-height:100vh;background:linear-gradient(135deg,#1a2d3d 0%,#1a5276 100%);display:flex;align-items:center;justify-content:center;padding:2rem;">
    <div style="width:100%;max-width:400px;">
        <div class="text-center mb-4">
            <div style="width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;font-size:28px;color:#fff;">
                <i class="bi bi-heart-fill" style="color:#e74c3c"></i>
            </div>
            <h4 style="color:#fff;font-weight:600;margin:0">Sistema Cáritas</h4>
            <p style="color:rgba(255,255,255,0.6);font-size:14px;margin-top:4px">Gestão Social Integrada</p>
        </div>
        <div class="card p-4">
            <h5 class="mb-4" style="font-size:16px;font-weight:600">Entrar na sua conta</h5>
            <form method="post">
                {% csrf_token %}
                {% if form.errors %}
                <div class="alert alert-danger py-2" style="font-size:13px">
                    Usuário ou senha incorretos.
                </div>
                {% endif %}
                <div class="mb-3">
                    <label class="form-label">Usuário</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-person"></i></span>
                        <input type="text" name="username" class="form-control" placeholder="Nome de usuário" required autofocus>
                    </div>
                </div>
                <div class="mb-4">
                    <label class="form-label">Senha</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-lock"></i></span>
                        <input type="password" name="password" class="form-control" placeholder="Senha" required>
                    </div>
                </div>
                <button type="submit" class="btn w-100" style="background:#1a5276;color:#fff;font-weight:500;padding:.65rem">
                    Entrar
                </button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 4. Refatorar `templates/estoque/listagem.html`

```html
{% extends 'base.html' %}
{% block title %}Estoque{% endblock %}
{% block page_title %}Estoque{% endblock %}
{% block breadcrumb %}
<li class="breadcrumb-item active">Estoque</li>
{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <p class="text-muted mb-0" style="font-size:14px">{{ itens.count }} item(ns) registrado(s)</p>
    {% if user.perfil == 'coordenador' or user.perfil == 'administrador' %}
    <a href="{% url 'estoque:entrada' %}" class="btn btn-sm" style="background:#1a5276;color:#fff">
        <i class="bi bi-plus-circle me-1"></i> Registrar entrada
    </a>
    {% endif %}
</div>

<div class="card">
    <div class="table-responsive">
        <table class="table table-hover mb-0">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Categoria</th>
                    <th>Quantidade</th>
                    <th>Validade</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for item in itens %}
                <tr class="{% if item.esta_vencido %}table-danger{% elif item.vence_em_breve %}table-warning{% endif %}">
                    <td><strong>{{ item.nome }}</strong></td>
                    <td>{{ item.get_categoria_display }}</td>
                    <td>{{ item.quantidade }} {{ item.unidade }}</td>
                    <td>{{ item.validade|date:"d/m/Y"|default:"—" }}</td>
                    <td>
                        {% if item.esta_vencido %}
                            <span class="badge" style="background:#fecaca;color:#991b1b">Vencido</span>
                        {% elif item.vence_em_breve %}
                            <span class="badge" style="background:#fef3c7;color:#92400e">Vence em breve</span>
                        {% else %}
                            <span class="badge" style="background:#dcfce7;color:#166534">OK</span>
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="5" class="text-center text-muted py-4" style="font-size:14px">
                        <i class="bi bi-box-seam" style="font-size:32px;display:block;margin-bottom:8px;opacity:.4"></i>
                        Nenhum item no estoque ainda.
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

---

## 5. Padrão para formulários (aplicar em `estoque/entrada.html`, `doacoes/registrar.html`, `familias/cadastro.html`)

Todo formulário deve seguir este padrão:

```html
{% extends 'base.html' %}
{% block content %}
<div style="max-width:720px">
    <form method="post">
        {% csrf_token %}

        <fieldset class="form-section">
            <legend>Seção</legend>
            {% for field in form %}
            <div class="mb-3">
                <label class="form-label" for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                    {% for error in field.errors %}
                    <div class="text-danger" style="font-size:12px;margin-top:4px">{{ error }}</div>
                    {% endfor %}
                {% endif %}
                {% if field.help_text %}
                    <div class="form-text">{{ field.help_text }}</div>
                {% endif %}
            </div>
            {% endfor %}
        </fieldset>

        <div class="d-flex gap-2">
            <button type="submit" class="btn" style="background:#1a5276;color:#fff;font-weight:500">
                <i class="bi bi-check-circle me-1"></i> Salvar
            </button>
            <a href="{{ cancelar_url }}" class="btn btn-outline-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```

Para formulários com múltiplas seções (como `familias/cadastro.html`), manter os `<fieldset>` separados por tema: Dados Pessoais, Dados Socioeconômicos, Composição Familiar, Dependentes.

---

## 6. Adicionar classes Bootstrap nos forms Django

Em cada `forms.py` do projeto, adicionar `attrs` com `class="form-control"` (ou `form-select` para dropdowns) para que os campos herdem o estilo correto:

```python
# Padrão para widgets em qualquer forms.py
widgets = {
    'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}),
    'categoria': forms.Select(attrs={'class': 'form-select'}),
    'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    'validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
}
```

Aplicar esse padrão em **todos** os `forms.py`: `accounts`, `familias`, `estoque`, `doacoes`.

---

## Instruções finais

- Substituir completamente os templates existentes — não mesclar com o antigo
- Bootstrap Icons já carregado no `base.html` via CDN — usar `<i class="bi bi-NOME">` em todos os ícones
- O layout sidebar + conteúdo só aparece para usuários autenticados; a página de login não usa o layout
- Manter todos os blocos Django (`{% block %}`, `{% url %}`, `{% if %}`, `{% for %}`) intactos
- Não criar arquivos CSS separados — todo o CSS fica no `<style>` do `base.html`
- Gerar todos os templates completos, sem trechos omitidos
