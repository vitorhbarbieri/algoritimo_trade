# 📊 Análise: Melhor Abordagem para Buscar Dividendos

## 🎯 Objetivo
Buscar dividendos automaticamente sem necessidade de importação manual.

## 🔍 Opções Analisadas

### Opção 1: API em Tempo Real (Sempre Buscar)
**Tecnologia:** Brapi.dev (já implementada)

**Vantagens:**
- ✅ Dados sempre atualizados
- ✅ Sem necessidade de armazenamento
- ✅ Código mais simples
- ✅ API gratuita e confiável

**Desvantagens:**
- ❌ Depende da API estar online
- ❌ Mais lento (requisição a cada consulta)
- ❌ Pode atingir rate limits
- ❌ Sem histórico se a API falhar

**Custo:** Gratuito (com limites de requisições)

---

### Opção 2: Web Scraping + Banco de Dados
**Tecnologia:** Scraping de Status Invest, Fundamentus, etc.

**Vantagens:**
- ✅ Dados públicos e gratuitos
- ✅ Sem limites de API
- ✅ Controle total

**Desvantagens:**
- ❌ Pode quebrar se o site mudar estrutura
- ❌ Mais complexo de manter
- ❌ Questões legais/éticas
- ❌ Pode ser bloqueado
- ❌ Mais lento (parsing HTML)

**Custo:** Gratuito, mas com riscos legais

---

### Opção 3: API + Cache no Banco (HÍBRIDA) ⭐ **RECOMENDADA**
**Tecnologia:** Brapi.dev + SQLite (armazenamento local)

**Vantagens:**
- ✅ Dados atualizados (busca periódica)
- ✅ Rápido (usa cache quando disponível)
- ✅ Histórico completo no banco
- ✅ Funciona mesmo se API estiver offline (dados em cache)
- ✅ Reduz carga na API
- ✅ Melhor experiência do usuário

**Desvantagens:**
- ⚠️ Precisa sincronizar periodicamente
- ⚠️ Usa espaço em disco (mínimo)

**Custo:** Gratuito

---

## 🏆 Decisão: Opção 3 (Híbrida)

### Como Funciona:
1. **Primeira busca:** Busca da API Brapi.dev e salva no banco
2. **Consultas subsequentes:** Usa dados do banco (rápido)
3. **Atualização automática:** 
   - Busca novos dividendos diariamente
   - Atualiza dados antigos se necessário
4. **Fallback:** Se API falhar, usa dados do banco

### Fluxo:
```
Usuário acessa portfolio
    ↓
Verifica se há dividendos no banco para o ticker
    ↓
Se SIM e recente (< 24h): Usa do banco ✅
    ↓
Se NÃO ou antigo (> 24h): Busca da API → Salva no banco → Usa ✅
```

### Benefícios:
- ⚡ **Performance:** Consultas instantâneas (dados locais)
- 🔄 **Atualização:** Dados sempre frescos (sincronização automática)
- 🛡️ **Resiliência:** Funciona mesmo se API estiver offline
- 📊 **Histórico:** Mantém histórico completo de dividendos
- 💰 **Custo:** Zero (API gratuita + armazenamento local)

---

## 📋 Implementação

### Estrutura do Banco:
```sql
CREATE TABLE dividendos (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    data_pagamento TEXT NOT NULL,
    valor_por_acao REAL NOT NULL,
    tipo TEXT DEFAULT 'DIVIDENDO',
    data_busca TEXT,  -- Quando foi buscado da API
    fonte TEXT DEFAULT 'brapi.dev',
    UNIQUE(ticker, data_pagamento, valor_por_acao)  -- Evita duplicatas
);
```

### Lógica de Sincronização:
1. **Ao carregar portfolio:**
   - Verifica últimos dividendos no banco
   - Se dados > 24h, busca atualização em background
   - Retorna dados do banco imediatamente

2. **Sincronização automática:**
   - Job diário (ex: meia-noite)
   - Busca novos dividendos para todas as ações da carteira
   - Atualiza banco silenciosamente

3. **Busca sob demanda:**
   - Botão "Atualizar Dividendos"
   - Força busca imediata da API

---

## ✅ Conclusão

**Recomendação:** Implementar **Opção 3 (Híbrida)**

**Por quê?**
- Melhor experiência do usuário (rápido + atualizado)
- Mais confiável (não depende 100% da API)
- Mantém histórico completo
- Custo zero
- Fácil de manter

**Próximos passos:**
1. Modificar código para usar banco como cache
2. Implementar sincronização automática
3. Adicionar verificação de dados antigos
4. Remover funcionalidade de importação manual (não mais necessária)

