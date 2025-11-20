# 📊 Análise Comparativa: APIs para Dividendos de Ações Brasileiras

## 🎯 Objetivo
Este documento apresenta alternativas à API **Brapi.dev** para obtenção de dados de dividendos de ações brasileiras (B3), com informações detalhadas para auxiliar na decisão de migração ou implementação de fallback.

---

## 📋 APIs Analisadas

### 1. **Brapi.dev** (Atual) ⭐
**Site:** https://brapi.dev  
**Status:** Em uso atualmente

#### ✅ Vantagens
- ✅ API gratuita disponível (com limitações)
- ✅ Open-source
- ✅ Documentação disponível
- ✅ Endpoint específico para dividendos: `?dividends=true`
- ✅ Retorna dados estruturados (cashDividends, stockDividends)
- ✅ Inclui data ex-dividendo (`lastDatePrior`)
- ✅ Suporte a API Key para planos pagos

#### ⚠️ Limitações
- ⚠️ Alguns tickers retornam 401 (Unauthorized) na versão gratuita
- ⚠️ Acesso a dividendos pode requerer plano pago (erro 403)
- ⚠️ Rate limiting não documentado (recomendado throttle de 1-2s)
- ⚠️ Dados podem ter atraso de alguns minutos
- ⚠️ Cobertura limitada para ações menos líquidas

#### 💰 Custos
- **Gratuito:** Limitado, alguns tickers bloqueados
- **Pago:** Preços não divulgados publicamente (verificar em brapi.dev/dashboard)

#### 📝 Endpoint
```
GET https://brapi.dev/api/quote/{TICKER}?dividends=true&token={API_KEY}
```

#### 🔧 Integração
- ✅ Já implementada no projeto
- ✅ Código em `data/dividendos_collector.py`

---

### 2. **HG Brasil Finance** 🆕
**Site:** https://hgbrasil.com/finance

#### ✅ Vantagens
- ✅ API brasileira especializada em dados da B3
- ✅ Suporte a dividendos
- ✅ Dados históricos disponíveis
- ✅ Cotações de moedas, índices e ações
- ✅ Possível plano gratuito (verificar site)

#### ⚠️ Limitações
- ⚠️ Documentação precisa ser verificada
- ⚠️ Limites de uso não claros
- ⚠️ Necessário cadastro para obter API key

#### 💰 Custos
- Verificar em: https://hgbrasil.com/finance
- Possível plano gratuito com limitações

#### 📝 Endpoint (Exemplo)
```
GET https://api.hgbrasil.com/finance/stock_price?key={API_KEY}&symbol={TICKER}
```

#### 🔧 Integração
- ⚠️ Requer implementação do zero
- ⚠️ Necessário verificar formato de resposta para dividendos

---

### 3. **IbovFinancials** 🆕
**Site:** https://ibovfinancials.com

#### ✅ Vantagens
- ✅ API gratuita
- ✅ Dados em tempo real da B3
- ✅ Suporte a dividendos mencionado
- ✅ Cotações de ações, FIIs, BDRs, índices
- ✅ Dados históricos disponíveis
- ✅ Integração com Excel/Google Sheets

#### ⚠️ Limitações
- ⚠️ Documentação precisa ser verificada
- ⚠️ Formato de resposta para dividendos não confirmado
- ⚠️ Possíveis limitações de rate limit

#### 💰 Custos
- **Gratuito:** Disponível (verificar limites)

#### 📝 Endpoint (Exemplo)
```
GET https://ibovfinancials.com/api/{endpoint}
```
*Endpoint específico precisa ser verificado na documentação*

#### 🔧 Integração
- ⚠️ Requer implementação do zero
- ⚠️ Necessário testar formato de resposta

---

### 4. **yfinance (Yahoo Finance)** 🆕
**Biblioteca Python:** `yfinance`  
**Documentação:** https://github.com/ranaroussi/yfinance

#### ✅ Vantagens
- ✅ Biblioteca Python gratuita e open-source
- ✅ Já está no `requirements.txt` do projeto
- ✅ Suporte a ações brasileiras (ticker.SA)
- ✅ Método `.dividends` disponível
- ✅ Sem necessidade de API key
- ✅ Dados históricos extensos
- ✅ Bem documentada e amplamente usada

#### ⚠️ Limitações
- ⚠️ Dados podem ter atraso de 15-20 minutos
- ⚠️ Yahoo Finance pode bloquear requisições excessivas
- ⚠️ Formato de dados pode ser diferente (pandas Series)
- ⚠️ Pode não incluir data ex-dividendo diretamente
- ⚠️ Dados podem ser menos completos que APIs especializadas

#### 💰 Custos
- **Gratuito:** Totalmente gratuito

#### 📝 Uso
```python
import yfinance as yf

ticker = yf.Ticker("PETR4.SA")
dividends = ticker.dividends  # Retorna pandas Series
dividend_history = ticker.dividends.to_dict()
```

#### 🔧 Integração
- ✅ Biblioteca já instalada
- ⚠️ Requer adaptação do código atual
- ⚠️ Formato de dados diferente (pandas Series vs dict)

---

### 5. **OkaneBox** 🆕
**Site:** https://www.okanebox.com.br

#### ✅ Vantagens
- ✅ API brasileira especializada
- ✅ Suporte a dividendos
- ✅ Dados de empresas brasileiras
- ✅ Exemplos em Python, R e Power BI

#### ⚠️ Limitações
- ⚠️ Documentação precisa ser verificada
- ⚠️ Custos não divulgados claramente
- ⚠️ Necessário cadastro

#### 💰 Custos
- Verificar em: https://www.okanebox.com.br

#### 📝 Endpoint
*Precisa ser verificado na documentação*

#### 🔧 Integração
- ⚠️ Requer implementação do zero

---

### 6. **Alpha Vantage** 🌍
**Site:** https://www.alphavantage.co

#### ✅ Vantagens
- ✅ API global bem estabelecida
- ✅ Documentação completa
- ✅ Planos gratuitos disponíveis
- ✅ Suporte a múltiplos mercados

#### ⚠️ Limitações
- ⚠️ Foco em mercado americano
- ⚠️ Cobertura limitada para ações brasileiras
- ⚠️ Rate limit restritivo no plano gratuito (5 calls/min, 500 calls/day)
- ⚠️ Dividendos podem não estar disponíveis para B3

#### 💰 Custos
- **Gratuito:** 5 requisições/min, 500/dia
- **Pago:** A partir de $49.99/mês

#### 📝 Endpoint
```
GET https://www.alphavantage.co/query?function=DIVIDENDS&symbol={TICKER}&apikey={API_KEY}
```

#### 🔧 Integração
- ⚠️ Cobertura brasileira limitada
- ⚠️ Não recomendado para ações B3

---

## 📊 Tabela Comparativa

| API | Gratuito | Cobertura B3 | Data Ex-Dividendo | Facilidade Integração | Status |
|-----|----------|--------------|-------------------|----------------------|--------|
| **Brapi.dev** | ✅ (limitado) | ✅✅✅ | ✅ | ✅✅✅ (já implementado) | ⭐ Atual |
| **HG Brasil** | ❓ | ✅✅✅ | ❓ | ⚠️ | 🆕 |
| **IbovFinancials** | ✅ | ✅✅✅ | ❓ | ⚠️ | 🆕 |
| **yfinance** | ✅ | ✅✅ | ⚠️ | ✅✅ | 🆕 |
| **OkaneBox** | ❓ | ✅✅✅ | ❓ | ⚠️ | 🆕 |
| **Alpha Vantage** | ✅ (limitado) | ⚠️ | ❓ | ✅ | ❌ Não recomendado |

**Legenda:**
- ✅✅✅ = Excelente
- ✅✅ = Bom
- ✅ = Aceitável
- ⚠️ = Limitado/Incerto
- ❓ = Não confirmado

---

## 🎯 Recomendações

### Opção 1: **Manter Brapi.dev + Fallback com yfinance** ⭐ (Recomendado)
**Vantagens:**
- ✅ Mantém código atual funcionando
- ✅ yfinance como fallback quando Brapi falhar (401/403)
- ✅ yfinance já está no projeto
- ✅ Cobertura ampla com duas fontes

**Implementação:**
1. Tentar Brapi.dev primeiro
2. Se retornar 401/403, usar yfinance como fallback
3. Registrar fonte no banco de dados

**Custo:** Gratuito

---

### Opção 2: **Migrar para HG Brasil ou IbovFinancials**
**Vantagens:**
- ✅ APIs especializadas em B3
- ✅ Possível melhor cobertura

**Desvantagens:**
- ⚠️ Requer reimplementação completa
- ⚠️ Necessário testar formato de dados
- ⚠️ Custos podem não ser claros

**Quando considerar:**
- Se Brapi.dev continuar com problemas de cobertura
- Se precisar de dados mais atualizados
- Se custos forem aceitáveis

---

### Opção 3: **Usar apenas yfinance**
**Vantagens:**
- ✅ Totalmente gratuito
- ✅ Biblioteca já instalada
- ✅ Sem necessidade de API key
- ✅ Cobertura razoável

**Desvantagens:**
- ⚠️ Dados podem ter atraso
- ⚠️ Pode não ter data ex-dividendo
- ⚠️ Formato de dados diferente

**Quando considerar:**
- Se Brapi.dev não for mais viável
- Se atraso de dados não for crítico
- Para simplificar dependências

---

## 🔍 Próximos Passos Sugeridos

1. **Testar APIs gratuitas:**
   - [ ] Testar yfinance com alguns tickers
   - [ ] Verificar formato de resposta
   - [ ] Confirmar disponibilidade de data ex-dividendo

2. **Avaliar APIs pagas:**
   - [ ] Verificar preços de HG Brasil
   - [ ] Verificar preços de IbovFinancials
   - [ ] Comparar com custos de Brapi.dev premium

3. **Implementar fallback:**
   - [ ] Adicionar função para yfinance em `dividendos_collector.py`
   - [ ] Implementar lógica de fallback automático
   - [ ] Testar com tickers problemáticos (ex: BBSE3)

4. **Documentar decisão:**
   - [ ] Atualizar este documento com resultados dos testes
   - [ ] Documentar formato de dados de cada API

---

## 📝 Notas Técnicas

### Formato de Dados Esperado
O código atual espera:
```python
{
    'data_pagamento': 'YYYY-MM-DD',
    'data_ex_dividendo': 'YYYY-MM-DD',  # CRÍTICO
    'ticker': 'PETR4',
    'valor_por_acao': 0.25,
    'tipo': 'DIVIDENDO' | 'JCP' | 'RENDIMENTO',
    'valor_total': 0.0  # Calculado depois
}
```

### Campos Críticos
- **data_ex_dividendo:** Essencial para calcular se o dividendo foi recebido
- **valor_por_acao:** Necessário para calcular valor total
- **data_pagamento:** Importante para registro

---

## 🔗 Links Úteis

- **Brapi.dev:** https://brapi.dev
- **HG Brasil:** https://hgbrasil.com/finance
- **IbovFinancials:** https://ibovfinancials.com
- **yfinance:** https://github.com/ranaroussi/yfinance
- **OkaneBox:** https://www.okanebox.com.br
- **Alpha Vantage:** https://www.alphavantage.co

---

## 📅 Data da Análise
**Data:** Janeiro 2025  
**Versão:** 1.0

---

## 💡 Conclusão

**Recomendação Principal:** Implementar **fallback com yfinance** mantendo Brapi.dev como fonte primária. Isso oferece:
- ✅ Redundância e confiabilidade
- ✅ Custo zero
- ✅ Cobertura ampla
- ✅ Implementação relativamente simples

**Próxima ação:** Testar yfinance com alguns tickers para validar formato e completude dos dados antes de implementar.


