# 🏗️ Arquitetura Multi-Tenant - Algoritimo Trade

## 🎯 Objetivo

Transformar o sistema em uma plataforma SaaS onde múltiplos clientes podem gerenciar suas próprias carteiras de forma isolada e segura.

---

## 📋 Componentes Necessários

### 1. **Sistema de Autenticação**
- Login/Registro de usuários
- Sessões seguras (Flask-Login ou JWT)
- Recuperação de senha
- Email de confirmação (opcional)

### 2. **Banco de Dados Multi-Tenant**
- Tabela `users` (usuários)
- Adicionar `user_id` em todas as tabelas:
  - `trades` → `user_id`
  - `dividendos` → `user_id`
- Índices para performance: `(user_id, ticker)`, `(user_id, trade_date)`

### 3. **Isolamento de Dados**
- Middleware para filtrar por `user_id` automaticamente
- Context manager para garantir isolamento
- Validação de permissões em todas as operações

### 4. **Interface Web**
- Página de login/registro
- Dashboard personalizado por usuário
- Logout
- Perfil do usuário

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nome TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,
    is_active INTEGER DEFAULT 1,
    is_admin INTEGER DEFAULT 0
);
```

### Tabela: `trades` (atualizada)
```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,  -- NOVO
    trade_date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY','SELL')),
    quantity REAL NOT NULL,
    price REAL NOT NULL,
    fees REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_trades_user_ticker ON trades (user_id, ticker);
CREATE INDEX idx_trades_user_date ON trades (user_id, trade_date);
```

### Tabela: `dividendos` (atualizada)
```sql
CREATE TABLE dividendos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,  -- NOVO
    data_pagamento TEXT NOT NULL,
    data_ex_dividendo TEXT,
    ticker TEXT NOT NULL,
    valor_por_acao REAL NOT NULL,
    quantidade_acoes REAL NOT NULL,
    valor_total REAL NOT NULL,
    tipo TEXT DEFAULT 'DIVIDENDO',
    data_busca TEXT,
    fonte TEXT DEFAULT 'brapi.dev',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, ticker, data_pagamento, valor_por_acao)  -- UNIQUE por usuário
);
CREATE INDEX idx_dividendos_user_ticker ON dividendos (user_id, ticker);
CREATE INDEX idx_dividendos_user_data ON dividendos (user_id, data_pagamento);
```

---

## 🔐 Sistema de Autenticação

### Opção 1: Flask-Login (Recomendado para início)
- ✅ Simples de implementar
- ✅ Integração fácil com Flask
- ✅ Sessões no servidor
- ⚠️ Requer cookies/sessões

### Opção 2: JWT (JSON Web Tokens)
- ✅ Stateless (escala melhor)
- ✅ Funciona bem com APIs
- ✅ Melhor para mobile/SPA
- ⚠️ Mais complexo

**Recomendação:** Começar com Flask-Login, migrar para JWT depois se necessário.

---

## 🛡️ Middleware de Isolamento

### Context Manager para Queries
```python
@contextmanager
def _connect(user_id: int = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        if user_id:
            # Aplicar filtro automático
            conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    finally:
        conn.commit()
        conn.close()
```

### Decorator para Isolamento
```python
def require_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'erro': 'Não autenticado'}), 401
        kwargs['user_id'] = current_user.id
        return f(*args, **kwargs)
    return decorated_function
```

---

## 📊 Fluxo de Dados

```
Usuário faz login
    ↓
Sessão criada (user_id armazenado)
    ↓
Todas as queries filtram por user_id automaticamente
    ↓
Dados isolados por usuário
    ↓
Logout → sessão destruída
```

---

## 🚀 Plano de Implementação

### Fase 1: Estrutura Base (Agora)
1. ✅ Criar tabela `users`
2. ✅ Adicionar `user_id` em `trades` e `dividendos`
3. ✅ Script de migração de dados existentes
4. ✅ Sistema de autenticação básico

### Fase 2: Isolamento (Próximo)
1. ✅ Middleware de isolamento
2. ✅ Atualizar todas as funções do repository
3. ✅ Decorators de autenticação
4. ✅ Testes de isolamento

### Fase 3: Interface (Depois)
1. ✅ Páginas de login/registro
2. ✅ Dashboard personalizado
3. ✅ Perfil do usuário
4. ✅ Recuperação de senha

### Fase 4: Melhorias (Futuro)
1. ⏳ Email de confirmação
2. ⏳ 2FA (autenticação de dois fatores)
3. ⏳ Planos/premium
4. ⏳ API keys para integração

---

## 🔒 Segurança

### Requisitos
- ✅ Senhas hasheadas (bcrypt ou similar)
- ✅ HTTPS obrigatório em produção
- ✅ Proteção CSRF
- ✅ Rate limiting em login
- ✅ Validação de inputs
- ✅ SQL injection prevention (usar ? placeholders)

### Boas Práticas
- ✅ Nunca retornar senhas em respostas
- ✅ Logs de acesso/erros
- ✅ Timeout de sessão
- ✅ Validação de email único

---

## 📈 Escalabilidade

### Curto Prazo (SQLite)
- ✅ Funciona bem até ~1000 usuários
- ✅ Fácil de migrar depois
- ✅ Zero configuração

### Médio Prazo (PostgreSQL)
- ✅ Melhor performance
- ✅ Suporte a mais usuários
- ✅ Features avançadas

### Longo Prazo (Distribuído)
- ✅ Sharding por região
- ✅ Cache (Redis)
- ✅ CDN para assets

---

## 💡 Vantagens da Arquitetura

1. **Isolamento Total:** Cada cliente vê apenas seus dados
2. **Escalável:** Pode crescer para milhares de usuários
3. **Seguro:** Dados protegidos por autenticação
4. **Profissional:** Pronto para produção/SaaS
5. **Flexível:** Fácil adicionar features (planos, premium, etc.)

---

## 🎯 Próximos Passos

1. Criar estrutura de autenticação
2. Migrar schema do banco
3. Atualizar repositories com user_id
4. Criar páginas de login/registro
5. Testar isolamento

---

**Status:** Proposta  
**Data:** Janeiro 2025  
**Versão:** 1.0

