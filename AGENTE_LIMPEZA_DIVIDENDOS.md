# 🧹 Agente de Limpeza de Dividendos Inválidos

## 📋 Descrição

Agente automático que remove dividendos inválidos do banco de dados. Um dividendo é considerado inválido quando sua **data ex-dividendo** é anterior à **primeira data de compra** do papel.

## 🎯 Problema Resolvido

Quando você compra uma ação, você só tem direito a receber dividendos cuja **data ex-dividendo** seja **posterior ou igual** à data da sua primeira compra. 

**Exemplo:**
- Você comprou ITUB4 em **2025-01-15**
- Há um dividendo com data ex-dividendo em **2025-01-10** (antes da compra)
- ❌ **Este dividendo é inválido** - você não tinha direito a ele

O agente identifica e remove automaticamente esses casos.

## ⚙️ Como Funciona

### 1. **Execução Automática**
O agente executa automaticamente **após cada sincronização de dividendos**:

```python
# Em data/dividendos_collector.py
# Após sincronizar dividendos, executa limpeza:
limpar_dividendos_invalidos()
```

### 2. **Processo de Limpeza**

Para cada ticker que tem dividendos no banco:

1. **Busca primeira compra:** Encontra a data da primeira compra (BUY) do ticker
2. **Verifica dividendos:** Para cada dividendo do ticker:
   - Compara `data_ex_dividendo` com `primeira_compra`
   - Se `data_ex_dividendo < primeira_compra` → **Remove o dividendo**
3. **Logs detalhados:** Registra todas as remoções

### 3. **Regras de Validação**

- ✅ **Válido:** `data_ex_dividendo >= primeira_compra`
- ❌ **Inválido:** `data_ex_dividendo < primeira_compra`
- ❌ **Inválido:** Se não há `data_ex_dividendo`, usa `data_pagamento` como referência
- ❌ **Inválido:** Se não há compras registradas, remove todos os dividendos do ticker

## 📊 Estatísticas Retornadas

O agente retorna um dicionário com:

```python
{
    "status": "ok",
    "tickers_verificados": 5,
    "total_verificados": 25,
    "total_removidos": 3,
    "removidos_por_ticker": {
        "ITUB4": 2,
        "PETR4": 1
    }
}
```

## 🔧 Uso Manual

### Via API (Dashboard)

```bash
POST /api/dividendos_limpar_invalidos
```

**Resposta:**
```json
{
    "status": "ok",
    "mensagem": "Limpeza concluída! 3 dividendos inválidos removidos.",
    "total_verificados": 25,
    "total_removidos": 3,
    "removidos_por_ticker": {
        "ITUB4": 2,
        "PETR4": 1
    }
}
```

### Via Python

```python
from data.trades_repository import limpar_dividendos_invalidos

resultado = limpar_dividendos_invalidos()
print(f"Removidos: {resultado['total_removidos']}")
```

## 📝 Logs

O agente gera logs detalhados:

```
🧹 [LIMPEZA] Iniciando limpeza de dividendos inválidos...
🔍 [LIMPEZA] Encontrados 5 tickers com dividendos: ['ITUB4', 'PETR4', ...]
📅 [LIMPEZA] ITUB4: Primeira compra em 2025-01-15
  🗑️  ITUB4: Dividendo 2025-01-10 (ex: 2025-01-08) removido - compra (2025-01-15) foi depois da data ex-dividendo
  ✅ ITUB4: 2 dividendos inválidos removidos
✅ [LIMPEZA] Limpeza concluída:
   - Tickers verificados: 5
   - Dividendos verificados: 25
   - Dividendos removidos: 3
```

## 🔄 Integração Automática

O agente é executado automaticamente em dois momentos:

1. **Após sincronização automática:** Quando `sincronizar_dividendos_automatico()` termina
2. **Via endpoint manual:** Quando você chama `/api/dividendos_limpar_invalidos`

## ⚠️ Observações Importantes

1. **Não destrutivo:** O agente só remove dividendos que claramente são inválidos
2. **Baseado em data ex-dividendo:** Usa `data_ex_dividendo` se disponível, senão usa `data_pagamento`
3. **Logs completos:** Todas as remoções são registradas para auditoria
4. **Idempotente:** Pode ser executado múltiplas vezes sem problemas

## 🐛 Tratamento de Erros

- Se houver erro ao processar um ticker, o agente continua com os próximos
- Erros são registrados nos logs mas não interrompem o processo
- Se não conseguir determinar primeira compra, remove todos os dividendos do ticker

## ✅ Benefícios

- ✅ **Dados corretos:** Remove dividendos que você não tinha direito
- ✅ **Automático:** Executa após cada sincronização
- ✅ **Auditável:** Logs detalhados de todas as ações
- ✅ **Seguro:** Não remove dados válidos

---

**Última atualização:** Janeiro 2025  
**Versão:** 1.0

