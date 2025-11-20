# 🚀 Guia de Deploy - Algoritimo Trade

Este guia explica como fazer deploy do projeto no GitHub e em serviços de hospedagem.

## 📋 Pré-requisitos

- Conta no GitHub
- Git instalado
- Conta em um serviço de hospedagem (Railway, Render, Heroku, etc.)

## 🔧 Passo 1: Configurar Git e GitHub

### 1.1 Inicializar Git

```bash
cd c:\Projetos\algoritimo_trade
git init
git add .
git commit -m "Initial commit: Sistema de trading algorítmico"
```

### 1.2 Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Crie um novo repositório (ex: `algoritimo-trade`)
3. **NÃO** inicialize com README, .gitignore ou license (já temos)

### 1.3 Conectar ao GitHub

```bash
git remote add origin https://github.com/SEU_USUARIO/algoritimo-trade.git
git branch -M main
git push -u origin main
```

### 1.4 Configurar Atualizações Automáticas

Para manter o repositório atualizado, sempre que fizer mudanças:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

## 🌐 Passo 2: Deploy em Produção

### Opção 1: Railway (Recomendado - Mais Fácil) ✅

**Railway** é gratuito e muito fácil de usar:

1. **Acesse:** https://railway.app
2. **Faça login** com GitHub
3. **Clique em "New Project"**
4. **Selecione "Deploy from GitHub repo"**
5. **Escolha seu repositório** `algoritimo-trade`
6. **Railway detecta automaticamente** o projeto Python
7. **Configure variáveis de ambiente** (se necessário):
   - `BRAPI_TOKEN` (se tiver)
   - `IBOVFINANCIALS_TOKEN` (se tiver)
   - `PORT` (gerenciado automaticamente)
8. **Deploy automático!** 🎉

**Vantagens:**
- ✅ Gratuito (com limites)
- ✅ Deploy automático do GitHub
- ✅ SSL automático
- ✅ Logs em tempo real
- ✅ Muito fácil de usar

---

### Opção 2: Render ✅

**Render** também é gratuito e fácil:

1. **Acesse:** https://render.com
2. **Faça login** com GitHub
3. **Clique em "New +" → "Web Service"**
4. **Conecte seu repositório** do GitHub
5. **Configure:**
   - **Name:** `algoritimo-trade`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python dashboard/app.py`
   - **Port:** `5000`
6. **Adicione variáveis de ambiente** (se necessário)
7. **Clique em "Create Web Service"**

**Vantagens:**
- ✅ Gratuito (com limites)
- ✅ Deploy automático
- ✅ SSL automático
- ✅ Fácil de usar

---

### Opção 3: Fly.io ✅

**Fly.io** é gratuito e poderoso:

1. **Instale Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Crie app:**
   ```bash
   fly launch
   ```

4. **Siga as instruções** na tela

**Vantagens:**
- ✅ Gratuito (com limites)
- ✅ Muito rápido
- ✅ Global CDN
- ✅ SSL automático

---

## 🔐 Variáveis de Ambiente

Configure estas variáveis no painel do seu serviço de hospedagem:

### Obrigatórias:
- Nenhuma (o projeto funciona sem tokens)

### Opcionais (para melhor performance):
- `BRAPI_TOKEN` - Token da API Brapi.dev
- `IBOVFINANCIALS_TOKEN` - Token da API IbovFinancials
- `PORT` - Porta (geralmente gerenciada automaticamente)

## 📝 Configuração do Banco de Dados

O projeto usa SQLite localmente. Para produção, você pode:

1. **Manter SQLite** (simples, mas limitado)
2. **Migrar para PostgreSQL** (recomendado para produção)

### Migrar para PostgreSQL:

1. Instale `psycopg2`:
   ```bash
   pip install psycopg2-binary
   ```

2. Adicione ao `requirements.txt`:
   ```
   psycopg2-binary>=2.9.0
   ```

3. Configure variável de ambiente:
   ```
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   ```

4. Atualize `trades_repository.py` para usar PostgreSQL

## 🔄 Atualizações Automáticas

### Railway e Render:
- ✅ Atualização automática ao fazer `git push`
- ✅ Deploy automático em cada commit

### Manual:
```bash
git add .
git commit -m "Sua mensagem"
git push
# Deploy automático acontece em alguns minutos
```

## 🐛 Troubleshooting

### Erro: "Port already in use"
- Verifique se a variável `PORT` está configurada
- O serviço geralmente define isso automaticamente

### Erro: "Module not found"
- Verifique se `requirements.txt` está completo
- Execute `pip install -r requirements.txt` localmente para testar

### Erro: "Database locked"
- SQLite pode ter problemas em produção
- Considere migrar para PostgreSQL

### App não inicia
- Verifique os logs no painel do serviço
- Verifique se `dashboard/app.py` está configurado corretamente
- Verifique se a porta está correta

## 📊 Monitoramento

### Railway:
- Acesse o dashboard em https://railway.app
- Veja logs em tempo real
- Monitore uso de recursos

### Render:
- Acesse o dashboard em https://render.com
- Veja logs e métricas
- Configure alertas

## 🔗 URLs de Produção

Após o deploy, você receberá uma URL como:
- Railway: `https://algoritimo-trade-production.up.railway.app`
- Render: `https://algoritimo-trade.onrender.com`
- Fly.io: `https://algoritimo-trade.fly.dev`

## ✅ Checklist de Deploy

- [ ] Git inicializado e conectado ao GitHub
- [ ] Repositório criado no GitHub
- [ ] Código commitado e pushado
- [ ] Conta criada no serviço de hospedagem
- [ ] Projeto conectado ao repositório GitHub
- [ ] Variáveis de ambiente configuradas (se necessário)
- [ ] Deploy realizado com sucesso
- [ ] URL de produção funcionando
- [ ] Testes realizados na URL de produção

## 🎉 Pronto!

Seu projeto está no ar! Qualquer atualização que você fizer e enviar para o GitHub será automaticamente deployada.

---

**Última atualização:** Janeiro 2025


