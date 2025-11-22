# 🤖 Agente Assessor de Investimentos

## 📋 Visão Geral

O **Agente Assessor de Investimentos** é um sistema completo de análise de carteira que realiza uma análise profunda e detalhada, emitindo pareceres fundamentados para cada ação e recomendações estratégicas abrangentes.

## 🎯 Funcionalidades

### 1. Análise Individual por Ação
- ✅ Parecer detalhado sobre a performance de cada ação
- ✅ Análise de rentabilidade (considerando dividendos)
- ✅ Avaliação do timing de compras/vendas
- ✅ Recomendação específica (MANTER, AUMENTAR, REDUZIR, VENDER)
- ✅ Justificativa fundamentada
- ✅ Perspectiva de curto/médio prazo
- ✅ Análise de yield de dividendos

### 2. Análise de Setores
- ✅ Avaliação da diversificação setorial
- ✅ Identificação de concentrações excessivas
- ✅ Sugestões de ajustes de alocação por setor
- ✅ Consideração de ciclos econômicos e tendências

### 3. Análise de Exposição
- ✅ Avaliação da concentração da carteira
- ✅ Cálculo do Índice de Herfindahl
- ✅ Identificação de riscos de concentração excessiva
- ✅ Sugestões de diversificação
- ✅ Avaliação do tamanho das posições

### 4. Análise de Performance
- ✅ Comparação de performance entre ações
- ✅ Ranking de melhores e piores performances
- ✅ Identificação de ações que contribuem positivamente
- ✅ Identificação de ações que prejudicam a carteira
- ✅ Avaliação da eficiência das operações (compras/vendas)

### 5. Análise de Dividendos
- ✅ Cálculo de yield de dividendos por ação
- ✅ Consideração de dividendos na rentabilidade total
- ✅ Identificação de ações com bom histórico de distribuição
- ✅ Análise de pagamentos recebidos

### 6. Recomendações Estratégicas
- ✅ Sugestões de rebalanceamento
- ✅ Oportunidades de otimização
- ✅ Alertas sobre riscos identificados
- ✅ Estratégias de longo prazo
- ✅ Próximos passos acionáveis

## 🔌 Endpoint da API

### GET `/api/assessor_investimentos`

**Autenticação:** Requerida (login)

**Resposta de Sucesso:**
```json
{
  "status": "ok",
  "analise_completa": {
    "resumo_executivo": "...",
    "pareceres_por_acao": [
      {
        "ticker": "PETR4",
        "parecer": "Análise detalhada...",
        "recomendacao": "MANTER",
        "justificativa": "...",
        "prioridade": "ALTA",
        "rentabilidade_atual": "15.5%",
        "rentabilidade_com_dividendos": "18.2%",
        "avaliacao_timing": "...",
        "perspectiva_curto_prazo": "...",
        "perspectiva_medio_prazo": "...",
        "yield_dividendos": "5.2%",
        "pontos_fortes": [...],
        "pontos_fracos": [...],
        "acao_sugerida": "Reduzir 30% da posição"
      }
    ],
    "analise_setores": {...},
    "analise_exposicao": {...},
    "analise_performance": {...},
    "recomendacoes_estrategicas": [...],
    "alertas": [...],
    "proximos_passos": [...]
  },
  "dados_estrutura": {...},
  "performance_acoes": {...},
  "analise_setores": {...},
  "timestamp": "2025-01-20T10:30:00"
}
```

**Resposta de Erro:**
```json
{
  "status": "erro",
  "erro": "Mensagem de erro",
  "mensagem": "Descrição do erro"
}
```

## 📊 Dados Analisados

O agente coleta e analisa:

1. **Posições Abertas**
   - Quantidade de ações
   - Preço médio de compra
   - Preço atual
   - Valor da posição
   - Rentabilidade

2. **Histórico de Operações**
   - Todas as compras realizadas
   - Todas as vendas realizadas
   - Timing das operações
   - Preços de compra/venda

3. **Dividendos Recebidos**
   - Total recebido por ação
   - Histórico de pagamentos
   - Yield de dividendos
   - Tipos de distribuição (DIVIDENDO, JCP, etc.)

4. **Métricas de Carteira**
   - PnL não realizado
   - PnL realizado
   - PnL total
   - Rentabilidades (carteira, realizada, total)
   - Exposição por ação
   - Concentração

5. **Análise Setorial**
   - Setor de cada ação
   - Exposição por setor
   - Diversificação setorial

## 🔧 Como Usar

### Via API (cURL)
```bash
curl -X GET http://localhost:5000/api/assessor_investimentos \
  -H "Cookie: session=..." \
  -H "Content-Type: application/json"
```

### Via JavaScript (Frontend)
```javascript
fetch('/api/assessor_investimentos', {
  method: 'GET',
  credentials: 'include'
})
.then(response => response.json())
.then(data => {
  console.log('Análise completa:', data);
  // Processar pareceres por ação
  data.analise_completa.pareceres_por_acao.forEach(parecer => {
    console.log(`${parecer.ticker}: ${parecer.recomendacao}`);
    console.log(`Justificativa: ${parecer.justificativa}`);
  });
});
```

### Via Python
```python
import requests

# Fazer login primeiro para obter sessão
session = requests.Session()
session.post('http://localhost:5000/auth/login', json={
    'email': 'seu@email.com',
    'password': 'sua_senha'
})

# Chamar assessor
response = session.get('http://localhost:5000/api/assessor_investimentos')
analise = response.json()

print("Resumo:", analise['analise_completa']['resumo_executivo'])
for parecer in analise['analise_completa']['pareceres_por_acao']:
    print(f"{parecer['ticker']}: {parecer['recomendacao']}")
```

## 🆚 Diferença entre `/api/ia_recomendacoes` e `/api/assessor_investimentos`

| Aspecto | `/api/ia_recomendacoes` | `/api/assessor_investimentos` |
|---------|------------------------|-------------------------------|
| **Análise** | Básica | Completa e profunda |
| **Dados usados** | Apenas posições atuais | Posições + trades + dividendos |
| **Pareceres** | Recomendações simples | Pareceres detalhados por ação |
| **Setores** | Não analisa | Análise completa de setores |
| **Exposição** | Não analisa | Análise de concentração |
| **Performance** | Básica | Detalhada com ranking |
| **Dividendos** | Não considera | Análise completa |
| **Recomendações** | Genéricas | Estratégicas e acionáveis |

## 📝 Estrutura do Parecer por Ação

Cada parecer inclui:

- **Parecer**: Análise detalhada e fundamentada
- **Recomendação**: MANTER, AUMENTAR, REDUZIR ou VENDER
- **Justificativa**: Explicação detalhada da recomendação
- **Prioridade**: ALTA, MÉDIA ou BAIXA
- **Rentabilidade Atual**: Percentual de rentabilidade
- **Rentabilidade com Dividendos**: Rentabilidade total incluindo dividendos
- **Avaliação de Timing**: Análise do timing de compras/vendas
- **Perspectiva Curto Prazo**: Expectativas para 3-6 meses
- **Perspectiva Médio Prazo**: Expectativas para 6-12 meses
- **Yield de Dividendos**: Percentual de yield
- **Pontos Fortes**: Lista de pontos positivos
- **Pontos Fracos**: Lista de pontos negativos
- **Ação Sugerida**: Recomendação específica e acionável

## ⚙️ Requisitos

- ✅ API de IA configurada (OpenAI ou Claude)
- ✅ Dados de operações importados
- ✅ Posições abertas na carteira
- ✅ (Opcional) Dividendos sincronizados

## 🚀 Exemplo de Uso Completo

```python
from core.investment_advisor import analisar_carteira_completa
from data.trades_repository import (
    positions_summary, list_trades, list_dividendos,
    calculate_realized_pnl
)

# Obter dados
positions = positions_summary(user_id=1)['positions']
trades = list_trades(user_id=1, limit=1000)
dividendos = list_dividendos(user_id=1, limit=1000)

# Calcular métricas
pnl_info = calculate_realized_pnl(user_id=1)
# ... calcular outras métricas ...

# Chamar assessor
resultado = analisar_carteira_completa(
    user_id=1,
    positions=positions,
    trades=trades,
    dividendos=dividendos,
    # ... outros parâmetros ...
)

# Processar resultado
if resultado['status'] == 'ok':
    analise = resultado['analise_completa']
    print("Resumo:", analise['resumo_executivo'])
    
    for parecer in analise['pareceres_por_acao']:
        print(f"\n{parecer['ticker']}:")
        print(f"  Recomendação: {parecer['recomendacao']}")
        print(f"  Justificativa: {parecer['justificativa']}")
        print(f"  Ação sugerida: {parecer['acao_sugerida']}")
```

## 📌 Notas Importantes

1. **Performance**: A análise completa pode levar alguns segundos devido à complexidade
2. **IA Necessária**: Requer API de IA configurada (OpenAI ou Claude)
3. **Dados Completos**: Quanto mais dados (trades, dividendos), melhor a análise
4. **Setores**: Usa mapeamento básico de setores conhecidos da B3

## 🔄 Atualizações Futuras

- [ ] Integração com API para obter setores reais
- [ ] Análise comparativa com benchmarks
- [ ] Análise de correlação entre ações
- [ ] Sugestões de novas ações baseadas em perfil
- [ ] Análise de risco (VaR, etc.)

