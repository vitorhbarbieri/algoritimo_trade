# 📦 Configuração do GitHub - Passo a Passo

## 🚀 Inicializar e Conectar ao GitHub

### Passo 1: Inicializar Git Localmente

```bash
# Navegar para o diretório do projeto
cd c:\Projetos\algoritimo_trade

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "Initial commit: Sistema de trading algorítmico com múltiplas APIs de dividendos"
```

### Passo 2: Criar Repositório no GitHub

1. **Acesse:** https://github.com/new
2. **Nome do repositório:** `algoritimo-trade` (ou outro nome de sua preferência)
3. **Descrição:** "Sistema completo de trading algorítmico modular com múltiplos agentes e estratégias"
4. **Visibilidade:** Escolha Public ou Private
5. **⚠️ IMPORTANTE:** NÃO marque nenhuma opção (README, .gitignore, license) - já temos esses arquivos
6. **Clique em "Create repository"**

### Passo 3: Conectar Repositório Local ao GitHub

```bash
# Adicionar remote (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/algoritimo-trade.git

# Renomear branch para main (se necessário)
git branch -M main

# Enviar código para GitHub
git push -u origin main
```

**Se pedir autenticação:**
- Use seu **username** e **Personal Access Token** (não sua senha)
- Para criar token: https://github.com/settings/tokens
- Permissões necessárias: `repo` (acesso completo aos repositórios)

### Passo 4: Verificar

1. Acesse seu repositório no GitHub: `https://github.com/SEU_USUARIO/algoritimo-trade`
2. Verifique se todos os arquivos estão lá
3. ✅ Pronto!

## 🔄 Como Manter Atualizado

Sempre que fizer mudanças no código:

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar mudanças
git add .

# 3. Fazer commit com mensagem descritiva
git commit -m "Descrição do que foi alterado"

# 4. Enviar para GitHub
git push
```

### Exemplos de Mensagens de Commit:

```bash
git commit -m "Adicionar sistema de fallback para APIs de dividendos"
git commit -m "Corrigir bugs na coleta de dividendos"
git commit -m "Atualizar documentação"
git commit -m "Melhorar tratamento de erros"
```

## 🔐 Configurar Autenticação (Se Necessário)

### Opção 1: Personal Access Token (Recomendado)

1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token" → "Generate new token (classic)"
3. Dê um nome: "Algoritimo Trade"
4. Selecione escopo: `repo` (acesso completo)
5. Clique em "Generate token"
6. **Copie o token** (só aparece uma vez!)
7. Use o token como senha quando o Git pedir

### Opção 2: GitHub CLI

```bash
# Instalar GitHub CLI
# Windows: https://cli.github.com/

# Login
gh auth login

# Agora pode usar git normalmente
git push
```

## 📋 Estrutura do Repositório

Seu repositório deve ter esta estrutura:

```
algoritimo-trade/
├── .gitignore          ✅ Arquivos ignorados
├── README.md           ✅ Documentação principal
├── requirements.txt    ✅ Dependências Python
├── Procfile            ✅ Para deploy (Heroku/Railway)
├── runtime.txt         ✅ Versão Python
├── DEPLOY.md           ✅ Guia de deploy
├── GITHUB_SETUP.md     ✅ Este arquivo
├── data/               ✅ Código fonte
├── dashboard/          ✅ Dashboard Flask
├── core/               ✅ Núcleo do sistema
├── features/           ✅ Features e indicadores
├── strategies/         ✅ Estratégias de trading
└── utils/              ✅ Utilitários
```

## ⚠️ Arquivos que NÃO vão para GitHub

O `.gitignore` já está configurado para ignorar:
- ✅ `.env` (variáveis de ambiente com tokens)
- ✅ `*.db` (bancos de dados)
- ✅ `__pycache__/` (cache Python)
- ✅ `venv/` (ambiente virtual)
- ✅ `.vscode/`, `.idea/` (configurações de IDE)

## 🔍 Verificar Status

```bash
# Ver status do repositório
git status

# Ver histórico de commits
git log --oneline

# Ver branches
git branch

# Ver remotes configurados
git remote -v
```

## 🐛 Problemas Comuns

### Erro: "remote origin already exists"
```bash
# Remover remote existente
git remote remove origin

# Adicionar novamente
git remote add origin https://github.com/SEU_USUARIO/algoritimo-trade.git
```

### Erro: "failed to push some refs"
```bash
# Fazer pull primeiro
git pull origin main --allow-unrelated-histories

# Depois fazer push
git push -u origin main
```

### Erro: "authentication failed"
- Verifique se está usando Personal Access Token (não senha)
- Crie um novo token em: https://github.com/settings/tokens

## 📚 Comandos Úteis

```bash
# Ver diferenças antes de commitar
git diff

# Ver histórico detalhado
git log --graph --oneline --all

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer mudanças em arquivo específico
git checkout -- arquivo.py

# Criar nova branch
git checkout -b nova-feature

# Voltar para main
git checkout main

# Mesclar branch
git merge nova-feature
```

## ✅ Checklist

- [ ] Git inicializado (`git init`)
- [ ] Arquivos adicionados (`git add .`)
- [ ] Primeiro commit feito (`git commit`)
- [ ] Repositório criado no GitHub
- [ ] Remote adicionado (`git remote add origin`)
- [ ] Código enviado (`git push`)
- [ ] Repositório visível no GitHub
- [ ] Autenticação configurada (se necessário)

## 🎉 Pronto!

Agora seu projeto está no GitHub e pode ser compartilhado, versionado e deployado facilmente!

---

**Última atualização:** Janeiro 2025


