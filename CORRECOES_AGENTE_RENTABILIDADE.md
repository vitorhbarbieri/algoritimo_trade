# 🔧 Correções: Agente de Limpeza e Fórmula de Rentabilidade

## 🐛 Problemas Identificados

### 1. Agente de Limpeza Falhando
- **Problema:** Dividendos da Petrobras (PETR4) e Itaú (ITUB4) estavam incorretos
- **Causa:** Comparação de datas usando strings diretamente (`data_referencia < primeira_compra`)
- **Impacto:** Comparação incorreta quando formatos eram diferentes ou havia problemas de parsing

### 2. Fórmula de Rentabilidade Incorreta
- **Problema:** Fórmula não estava considerando corretamente todos os componentes
- **Requisito:** Rentabilidade deve considerar:
  - (preço atual - preço médio) * quantidade atual
  - Dividendos recebidos (já calculados com quantidade correta no momento)
  - Lucro das vendas realizadas

---

## ✅ Correções Aplicadas

### 1. Agente de Limpeza Corrigido

**Arquivo:** `data/trades_repository.py` - função `limpar_dividendos_invalidos()`

**Mudanças:**
- ✅ Usa `datetime` para comparar datas corretamente
- ✅ Parseia primeira compra uma vez antes do loop
- ✅ Tenta múltiplos formatos de data para parsing robusto
- ✅ Remove dividendos onde `data_ex_dividendo < primeira_compra`
- ✅ Também remove se comprou no mesmo dia da data ex-dividendo (não tem direito)

**Código:**
```python
# Converter primeira compra para datetime uma vez
primeira_compra_dt = dt.strptime(primeira_compra, "%Y-%m-%d").date()

# Para cada dividendo, parsear e comparar corretamente
data_ref_dt = dt.strptime(data_referencia, "%Y-%m-%d").date()
if data_ref_dt < primeira_compra_dt:
    # Remover dividendo inválido
```

**Também corrigido em:** `data/dividendos_collector.py` - função `sincronizar_dividendos_automatico()`

---

### 2. Fórmula de Rentabilidade Corrigida

**Arquivo:** `dashboard/app.py` - função `portfolio_resumo()`

**Fórmula Corrigida:**
```python
# PnL da carteira (posições abertas) = (preço atual - preço médio) * quantidade atual
pnl_carteira = total_valor - total_investido

# PnL total = PnL não realizado + Dividendos + PnL realizado
pnl_total = pnl_carteira + total_dividendos + pnl_realizado

# Rentabilidade total = PnL total / Investimento total
rentabilidade_total = (pnl_total / investimento_total) if investimento_total > 0 else 0.0
```

**Componentes:**
1. **PnL Carteira:** `(preço atual - preço médio) * quantidade atual`
   - Lucro/prejuízo não realizado das posições abertas

2. **Dividendos:** `total_dividendos`
   - Já calculados com quantidade correta no momento do dividendo
   - Usa `calcular_quantidade_acoes_na_data()` para cada dividendo

3. **PnL Realizado:** `pnl_realizado`
   - Lucro/prejuízo das vendas já executadas
   - Calculado usando método FIFO

**Investimento Total:**
```python
investimento_total = total_investido + custo_vendas
```
- `total_investido`: Investido em posições abertas
- `custo_vendas`: Custo das ações vendidas

---

## 📊 Exemplo de Cálculo

**Cenário:**
- Comprou 100 ações de ITUB4 a R$ 30,00 (investido: R$ 3.000)
- Preço atual: R$ 32,00
- Recebeu R$ 50 em dividendos (com 100 ações)
- Vendeu 20 ações a R$ 31,00 (custo: R$ 600, receita: R$ 620)

**Cálculo:**
1. **PnL Carteira:** (32,00 - 30,00) * 80 = R$ 160
2. **Dividendos:** R$ 50
3. **PnL Realizado:** 620 - 600 = R$ 20
4. **PnL Total:** 160 + 50 + 20 = R$ 230
5. **Investimento Total:** 3.000 + 600 = R$ 3.600
6. **Rentabilidade:** 230 / 3.600 = 6,39%

---

## 🔍 Validação dos Dividendos

Os dividendos já são calculados corretamente durante a sincronização:

1. **Verifica data ex-dividendo:** Só importa se `primeira_compra < data_ex_dividendo`
2. **Calcula quantidade correta:** Usa `calcular_quantidade_acoes_na_data(ticker, data_ex_dividendo)`
3. **Valor total:** `valor_por_acao * quantidade_acoes` na data ex-dividendo

O agente de limpeza agora garante que dividendos inválidos sejam removidos mesmo após importação.

---

## 🧪 Como Testar

### 1. Testar Agente de Limpeza

```python
from data.trades_repository import limpar_dividendos_invalidos

resultado = limpar_dividendos_invalidos()
print(f"Removidos: {resultado['total_removidos']}")
print(f"Por ticker: {resultado['removidos_por_ticker']}")
```

### 2. Verificar Rentabilidade

```bash
GET http://localhost:5000/api/portfolio_resumo
```

Verificar campos:
- `pnl_carteira`: Lucro não realizado
- `total_dividendos`: Dividendos recebidos
- `pnl_realizado`: Lucro das vendas
- `pnl_total`: Soma de todos
- `rentabilidade`: PnL total / Investimento total

---

## 📝 Logs Esperados

**Agente de Limpeza:**
```
🧹 [LIMPEZA] Iniciando limpeza de dividendos inválidos...
📅 [LIMPEZA] PETR4: Primeira compra em 2025-01-15
  🗑️  PETR4: Dividendo 2025-01-10 (ex: 2025-01-08) removido - data ex (2025-01-08) é anterior à primeira compra (2025-01-15)
  ✅ PETR4: 2 dividendos inválidos removidos
```

**Sincronização:**
```
📅 [DIVIDENDOS] ITUB4: Primeira compra em 2025-01-15
  ⏭️  Dividendo 2025-01-10 (ex: 2025-01-08) ignorado - compra (2025-01-15) foi na ou depois da data ex-dividendo (2025-01-08)
```

---

## ✅ Resultado

- ✅ Agente de limpeza funciona corretamente para todos os tickers (PETR4, ITUB4, etc.)
- ✅ Comparação de datas usando datetime (robusto e correto)
- ✅ Fórmula de rentabilidade considera todos os componentes
- ✅ Dividendos já calculados com quantidade correta no momento

---

**Última atualização:** Janeiro 2025  
**Versão:** 2.0

