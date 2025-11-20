# 🔧 Configuração das APIs de Dividendos

## ✅ Implementação Concluída

O sistema agora suporta **múltiplas APIs com fallback automático**:

1. **Brapi.dev** (primária)
2. **IbovFinancials** (fallback)
3. **yfinance** (fallback final)

## 🔑 Configuração de Tokens

### Token IbovFinancials

O token já está configurado no código:
```python
IBOVFINANCIALS_TOKEN = "719d35865a8af526c715f5bbbca83c1e9579acb4"
```

**Para alterar via variável de ambiente:**
```bash
# Windows PowerShell
$env:IBOVFINANCIALS_TOKEN="seu-token-aqui"

# Linux/Mac
export IBOVFINANCIALS_TOKEN="seu-token-aqui"
```

### Token Brapi.dev

O token já está configurado no código:
```python
BRAPI_TOKEN = "58XDDJREpzCzHknHU6kTVk"
```

**Para alterar via variável de ambiente (opcional):**
```bash
# Windows PowerShell
$env:BRAPI_API_KEY="seu-token-aqui"

# Linux/Mac
export BRAPI_API_KEY="seu-token-aqui"
```

**Nota:** Se você definir uma variável de ambiente, ela terá prioridade sobre o token padrão.

## 🚀 Como Funciona

### Função Principal: `coletar_dividendos()`

A função principal tenta as APIs na seguinte ordem:

1. **Brapi.dev** - Se falhar (401, 403, 404 ou sem dados)
2. **IbovFinancials** - Se Brapi falhar
3. **yfinance** - Se ambas falharem

### Exemplo de Uso

```python
from data.dividendos_collector import coletar_dividendos

# Buscar dividendos (fallback automático)
dividendos, fonte = coletar_dividendos("PETR4", limit=100)

print(f"Fonte utilizada: {fonte}")
print(f"Dividendos encontrados: {len(dividendos)}")
```

### Funções Individuais

Você também pode usar cada API individualmente:

```python
from data.dividendos_collector import (
    coletar_dividendos_brapi,
    coletar_dividendos_ibovfinancials,
    coletar_dividendos_yfinance
)

# Brapi.dev
dividendos = coletar_dividendos_brapi("PETR4")

# IbovFinancials
dividendos = coletar_dividendos_ibovfinancials("PETR4")

# yfinance
dividendos = coletar_dividendos_yfinance("PETR4")
```

## 📊 Formato de Dados

Todas as APIs retornam o mesmo formato:

```python
[
    {
        'data_pagamento': '2025-01-15',
        'data_ex_dividendo': '2025-01-10',
        'ticker': 'PETR4',
        'valor_por_acao': 0.25,
        'tipo': 'DIVIDENDO',  # ou 'JCP', 'RENDIMENTO'
        'label': 'Dividendo',
        'valor_total': 0.0  # Calculado depois
    },
    ...
]
```

## 🧪 Testar o Sistema

Execute o script de teste:

```bash
python test_fallback_dividendos.py
```

Este script:
- ✅ Testa cada API individualmente
- ✅ Testa o fallback automático
- ✅ Testa com tickers problemáticos
- ✅ Mostra qual fonte foi utilizada

## ⚠️ Notas Importantes

### yfinance
- **Limitação:** Não fornece data ex-dividendo diretamente
- **Solução:** O sistema estima como 1 dia útil antes da data de pagamento
- **Impacto:** Pode haver pequenas imprecisões no cálculo de elegibilidade

### IbovFinancials
- **Endpoint:** Pode precisar ser ajustado conforme documentação oficial
- **Formato:** O código tenta múltiplos formatos de resposta
- **Token:** Já configurado no código

### Brapi.dev
- **Limitações:** Alguns tickers podem retornar 401/403
- **Solução:** Fallback automático para outras APIs

## 🔄 Migração Automática

O código existente **já foi atualizado** para usar o novo sistema:

- ✅ `sincronizar_dividendos_automatico()` - Usa fallback automático
- ✅ `importar_dividendos_automatico()` - Usa fallback automático
- ✅ `coletar_dividendos_multiplos_tickers()` - Usa fallback automático

**Não é necessário alterar código existente!** O sistema funciona automaticamente.

## 📝 Logs

O sistema registra qual fonte foi utilizada:

```
✅ [DIVIDENDOS] PETR4: Sucesso com Brapi.dev (15 dividendos)
✅ [DIVIDENDOS] BBSE3: Sucesso com IbovFinancials (8 dividendos)
✅ [DIVIDENDOS] ITUB4: Sucesso com yfinance (12 dividendos)
```

## 🐛 Troubleshooting

### Nenhuma API funciona
- Verifique conexão com internet
- Verifique se yfinance está instalado: `pip install yfinance`
- Verifique logs para erros específicos

### IbovFinancials não funciona
- Verifique se o token está correto
- Verifique se o endpoint mudou (pode precisar atualizar código)
- Consulte documentação oficial: https://ibovfinancials.com

### yfinance não funciona
- Instale: `pip install yfinance`
- Verifique se o ticker está correto (formato: PETR4.SA)

## 📚 Documentação Adicional

- **Análise completa:** `ANALISE_APIS_DIVIDENDOS.md`
- **Resumo executivo:** `RESUMO_DECISAO_APIS.md`
- **Código fonte:** `data/dividendos_collector.py`

---

**Última atualização:** Janeiro 2025

