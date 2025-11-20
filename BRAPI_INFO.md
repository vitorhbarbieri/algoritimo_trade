# 📊 Informações sobre a API Brapi.dev

## 🌐 Site Oficial
**URL:** https://brapi.dev

## 📋 Sobre a API

A Brapi.dev é uma API gratuita e open-source que fornece dados financeiros da B3 (Bolsa de Valores brasileira).

### ✅ Versão Gratuita (Atual)

**Características:**
- ✅ Gratuita e sem necessidade de cadastro
- ✅ Sem limite de requisições (mas com throttling recomendado)
- ✅ Dados de cotações em tempo real
- ✅ Histórico de preços
- ✅ **Dividendos disponíveis** (com parâmetro `?dividends=true`)

**Limitações:**
- ⚠️ Alguns tickers podem retornar 401 (Unauthorized) - especialmente ações menos líquidas
- ⚠️ Rate limiting não documentado (recomenda-se throttle de 1-2 segundos entre requisições)
- ⚠️ Dados podem ter atraso de alguns minutos

**Endpoint de Dividendos:**
```
GET https://brapi.dev/api/quote/{TICKER}?dividends=true
```

**Exemplo:**
```bash
curl "https://brapi.dev/api/quote/PETR4?dividends=true"
```

**Resposta:**
```json
{
  "results": [{
    "symbol": "PETR4",
    "dividendsData": {
      "cashDividends": [
        {
          "paymentDate": "2025-09-22T00:00:00.000Z",
          "rate": 0.30845,
          "label": "DIVIDENDO",
          "lastDatePrior": "2025-06-02T00:00:00.000Z"
        }
      ],
      "stockDividends": [],
      "subscriptions": []
    }
  }]
}
```

---

## 💰 Versão Paga (Premium)

### 🔍 Como Funciona

**Site para informações:** https://brapi.dev  
**Dashboard:** https://brapi.dev/dashboard

**Características da versão paga:**
- ✅ API Key para autenticação
- ✅ Maior limite de requisições
- ✅ Acesso a todos os tickers (sem erros 401)
- ✅ **Acesso a dividendos** (requer plano pago)
- ✅ Dados em tempo real mais rápidos
- ✅ Suporte prioritário
- ✅ Endpoints adicionais

### ⚠️ Importante sobre Dividendos

**Erro 403:** Se você receber erro 403 ao buscar dividendos, significa que seu plano atual não permite acesso a dados de dividendos. É necessário fazer upgrade para um plano pago.

**Mensagem de erro:**
```json
{
  "error": true,
  "message": "O seu plano não permite acessar dados de dividendos. Por favor, considere fazer um upgrade para um plano pago em brapi.dev/dashboard"
}
```

**Solução:**
1. Acesse https://brapi.dev/dashboard
2. Faça upgrade para um plano que inclua acesso a dividendos
3. A chave da API continuará a mesma

### 📝 Como Obter API Key

1. **Acesse:** https://brapi.dev
2. **Cadastre-se** ou faça login
3. **Navegue até a seção de API Keys**
4. **Gere uma nova chave**
5. **Configure no projeto:**

**Via variável de ambiente:**
```bash
# Windows PowerShell
$env:BRAPI_API_KEY="sua-chave-aqui"

# Linux/Mac
export BRAPI_API_KEY="sua-chave-aqui"
```

**Via arquivo .env:**
```
BRAPI_API_KEY=sua-chave-aqui
```

### 🔧 Como Usar a API Key

**Endpoint com autenticação:**
```
GET https://brapi.dev/api/quote/{TICKER}?dividends=true&token={API_KEY}
```

**Exemplo:**
```bash
curl "https://brapi.dev/api/quote/BBSE3?dividends=true&token=sua-chave-aqui"
```

---

## ⚠️ Tickers com Erro 401

Alguns tickers retornam erro 401 (Unauthorized) na versão gratuita:
- BBSE3
- Outros tickers menos líquidos

**Soluções:**
1. **Usar versão paga** (recomendado para produção)
2. **Tentar sem sufixo .SA** (alguns funcionam)
3. **Usar API alternativa** como fallback

---

## 🔄 Fallback Implementado

O sistema atual:
1. Tenta buscar da Brapi.dev
2. Se retornar 401, registra no log e continua
3. Processa apenas tickers que retornam dados

---

## 📚 Documentação Completa

Para mais informações, acesse:
- **Site:** https://brapi.dev
- **Documentação:** https://brapi.dev/docs (se disponível)
- **GitHub:** https://github.com/brunobastosg/brapi (se disponível)

---

## 💡 Recomendações

1. **Para desenvolvimento/testes:** Versão gratuita é suficiente
2. **Para produção:** Considere a versão paga para:
   - Acesso garantido a todos os tickers
   - Maior confiabilidade
   - Suporte prioritário

3. **Throttling:** Sempre mantenha intervalo de 1-2 segundos entre requisições

