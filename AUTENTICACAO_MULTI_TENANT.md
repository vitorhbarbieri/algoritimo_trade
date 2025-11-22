# Sistema de Autenticação Multi-Tenant

## ✅ Implementação Completa

O sistema agora possui autenticação completa com isolamento de dados por usuário.

## 🚀 Como Usar

### 1. Iniciar o Servidor

Execute o script PowerShell:
```powershell
.\iniciar_com_auth.ps1
```

Ou manualmente:
```bash
cd dashboard
python app.py
```

### 2. Acessar o Sistema

Abra no navegador: **http://localhost:5000**

### 3. Fazer Login

**Credenciais Padrão:**
- Email: `admin@algoritimo.com`
- Senha: `admin123`

Ou crie uma nova conta em: **http://localhost:5000/auth/register**

## 📋 Funcionalidades

### Autenticação
- ✅ Login/Registro de usuários
- ✅ Sessão persistente (Flask-Login)
- ✅ Proteção de todas as rotas
- ✅ Isolamento automático de dados por usuário

### Isolamento de Dados
- ✅ Cada usuário vê apenas seus próprios dados
- ✅ Trades isolados por `user_id`
- ✅ Dividendos isolados por `user_id`
- ✅ Cálculos de rentabilidade por usuário

### Rotas Protegidas
Todas as rotas da API agora exigem login:
- `/api/status`
- `/api/analisar/<ticker>`
- `/api/trades`
- `/api/portfolio_resumo`
- `/api/importar_operacoes`
- `/api/dividendos`
- `/api/ia_recomendacoes`
- E todas as demais rotas...

## 🔧 Estrutura de Arquivos

```
auth/
  ├── models.py          # Modelo de usuário e autenticação
  └── auth_routes.py     # Rotas de login/registro/logout

dashboard/
  ├── app.py             # Aplicação Flask (atualizada com @login_required)
  └── templates/
      ├── login.html      # Página de login
      ├── register.html   # Página de registro
      └── home.html       # Dashboard (atualizado com link de logout)

data/
  ├── migrate_multi_tenant.py  # Script de migração do banco
  └── trades_repository.py     # Funções atualizadas com user_id

iniciar_com_auth.ps1     # Script para iniciar servidor
```

## 🗄️ Banco de Dados

### Migração Automática
O script `migrate_multi_tenant.py` foi executado e:
- ✅ Criou tabela `users`
- ✅ Adicionou `user_id` em `trades`
- ✅ Adicionou `user_id` em `dividendos`
- ✅ Migrou dados existentes para `user_id=1`
- ✅ Criou usuário padrão (admin@algoritimo.com)

### Schema Atualizado
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nome TEXT,
    created_at TEXT,
    last_login TEXT,
    is_active INTEGER DEFAULT 1,
    is_admin INTEGER DEFAULT 0
);

CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,  -- NOVO
    trade_date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    ...
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE dividendos (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,  -- NOVO
    data_pagamento TEXT NOT NULL,
    ...
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🔐 Segurança

- ✅ Senhas hash com Werkzeug
- ✅ Sessões seguras (SECRET_KEY)
- ✅ Proteção CSRF (Flask-Login)
- ✅ Isolamento de dados no nível do banco

## 📝 Notas Importantes

1. **Dados Existentes**: Todos os dados existentes foram migrados para `user_id=1` (usuário admin padrão)

2. **Novos Usuários**: Cada novo usuário terá seus próprios dados isolados

3. **Compatibilidade**: Funções antigas ainda funcionam com `user_id=None` (usam `user_id=1` como fallback)

4. **Logout**: Use o botão "Sair" no header ou acesse `/auth/logout`

## 🧪 Testando

1. Crie múltiplas contas
2. Importe operações diferentes em cada conta
3. Verifique que cada usuário vê apenas seus dados
4. Teste logout/login

## 🐛 Troubleshooting

Se encontrar erros:
1. Execute a migração novamente: `python data/migrate_multi_tenant.py`
2. Verifique se Flask-Login está instalado: `pip install flask-login`
3. Limpe o cache Python: `Get-ChildItem -Path . -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force`

