# 📊 RELATÓRIO COMPLETO - Sistema de Trading com Agentes Cooperativos

**Data:** $(Get-Date -Format "dd/MM/yyyy HH:mm")  
**Projeto:** Algoritimo Trade Agentes  
**Versão:** 1.0.0

---

## 📋 SUMÁRIO EXECUTIVO

Este documento descreve detalhadamente o funcionamento do sistema de trading algorítmico baseado em agentes cooperativos. O sistema utiliza dois agentes principais (TraderAgent e RiskAgent) que trabalham em conjunto para identificar oportunidades de mercado através de 5 modelos de assimetria diferentes, executar trades com controle de risco rigoroso e monitorar o mercado em tempo real.

---

## 🏗️ ARQUITETURA DO SISTEMA

### Componentes Principais

```
┌─────────────────────────────────────────────────────────────┐
│                    DASHBOARD CENTRAL                         │
│              (Streamlit - Interface Web)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   API SERVER (Flask)                        │
│         Endpoints REST para controle do sistema             │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Monitoring   │ │  Backtest    │ │   Agents     │
│   Service    │ │   Engine     │ │  (Trader +   │
│              │ │              │ │   Risk)      │
└──────────────┘ └──────────────┘ └──────────────┘
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Market     │ │   Portfolio  │ │  Execution   │
│   Monitor    │ │   Manager    │ │  Simulator   │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Fluxo de Dados

1. **Coleta de Dados** → APIs de mercado (yfinance, Binance)
2. **Análise de Assimetrias** → MarketMonitor identifica oportunidades
3. **Geração de Propostas** → TraderAgent cria ordens
4. **Validação de Risco** → RiskAgent avalia e aprova/rejeita
5. **Execução** → ExecutionSimulator simula execução
6. **Atualização de Portfólio** → PortfolioManager atualiza posições
7. **Monitoramento** → Dashboard exibe resultados em tempo real

---

## 🤖 AGENTES DO SISTEMA

### 1. TraderAgent (Agente Criativo)

**Função:** Gerar propostas de trading baseadas em oportunidades identificadas.

**Responsabilidades:**
- Analisar dados de mercado em tempo real
- Identificar assimetrias usando os 5 modelos
- Criar propostas de ordens (OrderProposal)
- Aplicar sizing (tamanho de posição) baseado em risco

**Estratégias Implementadas:**
- **Delta-Hedged Volatility Arbitrage**: Operações com opções delta-neutras
- **Pairs/Statistical Arbitrage**: Operações em pares de ativos cointegrados

**Configurações (config.json):**
```json
{
  "enable_vol_arb": true,
  "enable_pairs": true,
  "vol_arb_size": 10,
  "pairs_size": 100
}
```

### 2. RiskAgent (Agente Controlador)

**Função:** Validar, filtrar e modificar propostas do TraderAgent para garantir controle de risco.

**Responsabilidades:**
- Verificar limites de exposição por ativo
- Validar gregos agregados (Delta, Gamma, Vega, Theta)
- Aplicar kill switch em caso de perdas excessivas
- Modificar tamanho de posição se necessário
- Rejeitar propostas que excedam limites

**Limites de Risco (config.json):**
```json
{
  "max_exposure": 0.5,           // Máximo 50% do NAV em exposição
  "max_delta": 1000,             // Limite de Delta agregado
  "max_gamma": 500,              // Limite de Gamma agregado
  "max_vega": 1000,              // Limite de Vega agregado
  "max_position_size": 10000,    // Tamanho máximo por posição
  "kill_switch_threshold": 0.15   // Kill switch se perda > 15%
}
```

**Decisões Possíveis:**
- ✅ **APPROVE**: Proposta aprovada sem modificações
- ⚠️ **MODIFY**: Proposta aprovada com tamanho reduzido
- ❌ **REJECT**: Proposta rejeitada por violar limites

### 3. PortfolioManager

**Função:** Gerenciar posições, NAV (Net Asset Value) e snapshots do portfólio.

**Responsabilidades:**
- Manter registro de todas as posições
- Calcular NAV em tempo real
- Criar snapshots periódicos para análise
- Calcular gregos agregados do portfólio

### 4. ExecutionSimulator

**Função:** Simular execução de ordens com slippage e comissões realistas.

**Responsabilidades:**
- Aplicar slippage baseado em volume e tamanho da ordem
- Calcular comissões
- Simular preenchimento parcial/total
- Registrar ordens e fills para análise

**Parâmetros:**
```json
{
  "base_slippage": 0.0005,        // 0.05% slippage base
  "slippage_k": 0.001,           // Multiplicador por tamanho
  "commission_rate": 0.0002      // 0.02% de comissão
}
```

---

## 🔍 MODELOS DE ASSIMETRIA DE MERCADO

O sistema implementa **5 modelos diferentes** para identificar oportunidades de trading:

### 1. Volatility Arbitrage (Arbitragem de Volatilidade)

**Teoria:** Opções com volatilidade implícita (IV) significativamente diferente da volatilidade histórica ou teórica.

**Como Funciona:**
1. Calcula volatilidade histórica do ativo subjacente
2. Compara com volatilidade implícita das opções
3. Identifica opções com IV muito alta ou muito baixa
4. Calcula preço teórico usando Black-Scholes
5. Compara preço teórico com preço de mercado
6. Identifica mispricing (diferença entre teórico e mercado)

**Assimetria Explorada:**
- IV de mercado ≠ IV histórica → Oportunidade de arbitragem
- Preço de mercado ≠ Preço teórico → Mispricing

**Exemplo:**
```
Ativo: AAPL
Spot: $150
Opção Call Strike $155, Expiry 30 dias
IV de Mercado: 35%
IV Histórica: 25%
Preço Teórico (BS): $2.50
Preço de Mercado: $3.20
Mispricing: +28% → Oportunidade de VENDA
```

**Implementação:** `MarketMonitor.scan_volatility_arbitrage()`

---

### 2. Pairs Trading / Statistical Arbitrage

**Teoria:** Dois ativos que historicamente se movem juntos (cointegrados) podem ter spreads temporários que revertem à média.

**Como Funciona:**
1. Identifica pares de ativos correlacionados (ex: AAPL e MSFT)
2. Calcula spread histórico entre os dois ativos
3. Testa cointegração usando teste de Engle-Granger
4. Calcula Z-score do spread atual
5. Quando Z-score > threshold, identifica oportunidade
6. Compra o ativo subvalorizado, vende o supervalorizado

**Assimetria Explorada:**
- Spread temporário entre ativos cointegrados
- Reversão à média do spread

**Exemplo:**
```
Par: AAPL / MSFT
Spread Médio Histórico: 0.05
Spread Atual: 0.15
Z-score: 2.5 (threshold: 2.0)
Ação: Vender spread (vender AAPL, comprar MSFT)
Expectativa: Spread reverte para 0.05
```

**Implementação:** `MarketMonitor.scan_pairs_trading()`

**Configuração:**
```json
{
  "pairs_ticker1": "AAPL",
  "pairs_ticker2": "MSFT",
  "pairs_lookback": 60,
  "pairs_zscore_threshold": 2.0
}
```

---

### 3. Spread Arbitrage (Arbitragem de Spread)

**Teoria:** Anomalias nos spreads bid-ask de um ativo indicam ineficiências de curto prazo.

**Como Funciona:**
1. Monitora spreads bid-ask em tempo real
2. Compara com spread médio histórico
3. Identifica spreads anormalmente largos ou estreitos
4. Spread largo → Oportunidade de market making
5. Spread estreito → Possível ineficiência de preço

**Assimetria Explorada:**
- Spread bid-ask anormal → Oportunidade de arbitragem
- Ineficiência de mercado de curto prazo

**Exemplo:**
```
Ativo: PETR4.SA
Bid Médio Histórico: R$ 28.50
Ask Médio Histórico: R$ 28.55
Spread Médio: R$ 0.05 (0.18%)

Bid Atual: R$ 28.45
Ask Atual: R$ 28.60
Spread Atual: R$ 0.15 (0.53%) → 3x maior que normal
Oportunidade: Market making (comprar no bid, vender no ask)
```

**Implementação:** `MarketMonitor.scan_spread_arbitrage()`

**Configuração:**
```json
{
  "spread_threshold": 0.5  // Spread deve ser 50% maior que normal
}
```

---

### 4. Momentum Opportunities (Oportunidades de Momentum)

**Teoria:** Ativos com forte movimento direcional sustentado por volume tendem a continuar na mesma direção.

**Como Funciona:**
1. Calcula retornos de curto prazo (ex: 5 dias)
2. Calcula retornos de médio prazo (ex: 20 dias)
3. Verifica volume acima da média
4. Identifica tendências fortes e sustentadas
5. Filtra por força do movimento (RSI, MACD)

**Assimetria Explorada:**
- Continuidade de tendências fortes
- Inércia de mercado

**Exemplo:**
```
Ativo: NVDA
Retorno 5 dias: +8%
Retorno 20 dias: +25%
Volume: 150% da média
RSI: 65 (forte, mas não sobrecomprado)
MACD: Positivo e crescente
Sinal: COMPRA (momentum de alta)
```

**Implementação:** `MarketMonitor.scan_momentum_opportunities()`

---

### 5. Mean Reversion (Reversão à Média)

**Teoria:** Ativos que se desviaram significativamente de sua média de preço tendem a retornar à média.

**Como Funciona:**
1. Calcula média móvel de preços (ex: 20 dias)
2. Calcula desvio padrão
3. Calcula Z-score do preço atual
4. Quando Z-score > threshold, identifica oportunidade
5. Preço muito alto → VENDA (espera queda)
6. Preço muito baixo → COMPRA (espera alta)

**Assimetria Explorada:**
- Desvios extremos de preço
- Reversão estatística à média

**Exemplo:**
```
Ativo: TSLA
Preço Atual: $180
Média 20 dias: $200
Desvio Padrão: $15
Z-score: -1.33 (preço 1.33 desvios abaixo da média)
Threshold: 2.0
Ação: Aguardar (ainda não atingiu threshold)

Se Z-score fosse -2.5:
Ação: COMPRA (preço muito abaixo da média, espera reversão)
```

**Implementação:** `MarketMonitor.scan_mean_reversion()`

**Configuração:**
```json
{
  "mean_reversion_threshold": 2.0  // Z-score de 2 desvios padrão
}
```

---

## 🔄 FLUXO DE PROCESSAMENTO

### Fluxo Principal (Backtest)

```
1. INICIALIZAÇÃO
   ├─ Carregar dados (spot, futures, options)
   ├─ Inicializar PortfolioManager (NAV inicial)
   ├─ Criar TraderAgent
   ├─ Criar RiskAgent
   └─ Criar ExecutionSimulator

2. PARA CADA DATA NO PERÍODO:
   ├─ Preparar dados de mercado para a data
   │
   ├─ TraderAgent gera propostas
   │  ├─ Analisa oportunidades de Vol Arb
   │  ├─ Analisa oportunidades de Pairs
   │  └─ Cria OrderProposal para cada oportunidade
   │
   ├─ PARA CADA PROPOSTA:
   │  ├─ RiskAgent avalia proposta
   │  │  ├─ Verifica limites de exposição
   │  │  ├─ Verifica gregos agregados
   │  │  ├─ Verifica kill switch
   │  │  └─ Retorna: APPROVE / MODIFY / REJECT
   │  │
   │  ├─ SE APPROVE ou MODIFY:
   │  │  ├─ ExecutionSimulator executa ordem
   │  │  │  ├─ Aplica slippage
   │  │  │  ├─ Calcula comissões
   │  │  │  └─ Retorna fill
   │  │  │
   │  │  └─ PortfolioManager atualiza posição
   │  │     ├─ Atualiza quantidade
   │  │     └─ Atualiza cash
   │  │
   │  └─ SE REJECT:
   │     └─ Registra motivo da rejeição
   │
   └─ PortfolioManager cria snapshot
      ├─ Calcula NAV atual
      ├─ Calcula valor das posições
      └─ Salva snapshot

3. FINALIZAÇÃO
   ├─ Calcula métricas (Sharpe, Max DD, etc.)
   ├─ Salva resultados em CSV
   └─ Retorna resultados
```

### Fluxo de Monitoramento em Tempo Real

```
1. MonitoringService inicia thread de monitoramento
   │
   ├─ LOOP (a cada 5 minutos):
   │  ├─ MarketMonitor.scan_market()
   │  │  ├─ Busca dados de mercado via APIs
   │  │  ├─ Executa os 5 modelos de assimetria
   │  │  └─ Retorna lista de oportunidades
   │  │
   │  ├─ PARA CADA OPORTUNIDADE:
   │  │  ├─ TraderAgent gera proposta
   │  │  ├─ RiskAgent avalia proposta
   │  │  └─ SE APROVADO:
   │  │     └─ ExecutionSimulator executa (ou envia para broker real)
   │  │
   │  └─ Atualiza status e oportunidades encontradas
   │
   └─ Dashboard exibe resultados em tempo real
```

---

## 📊 DASHBOARD CENTRAL

### Abas Disponíveis

1. **📊 Visão Geral**
   - Status do sistema
   - Métricas principais (P&L, Sharpe, Max DD)
   - Gráficos de performance

2. **🤖 Atividade dos Agentes**
   - Propostas geradas pelo TraderAgent
   - Avaliações do RiskAgent
   - Decisões (APPROVE/REJECT/MODIFY)
   - Motivos de rejeição

3. **💰 Portfólio**
   - Posições atuais
   - NAV em tempo real
   - Exposição por ativo
   - Gregos agregados

4. **📈 Backtest**
   - Executar novos backtests
   - Visualizar resultados históricos
   - Comparar estratégias

5. **📋 Ações Monitoradas**
   - Lista de 30 ações (15 BR + 15 US)
   - Status de cada ação
   - Oportunidades identificadas

6. **📝 Log de Monitoramento**
   - Logs em tempo real
   - Propostas → Avaliações → Execuções
   - Oportunidades encontradas
   - Feedback das ações

### Controles Disponíveis

- **▶️ Iniciar Monitoramento**: Inicia scan contínuo do mercado
- **⏸️ Parar Monitoramento**: Para o scan
- **🔍 Scan Manual**: Executa scan único imediato
- **🔄 Executar Backtest**: Roda backtest completo

---

## 📈 MÉTRICAS CALCULADAS

### Métricas de Performance

- **Total Return**: Retorno total do período
- **Sharpe Ratio**: Retorno ajustado por risco
- **Max Drawdown**: Maior queda do NAV
- **Volatility**: Volatilidade dos retornos
- **Win Rate**: Percentual de trades lucrativos
- **Total Trades**: Número total de trades executados

### Métricas de Risco

- **Exposição Total**: % do NAV em posições
- **Greeks Agregados**: Delta, Gamma, Vega, Theta totais
- **VaR (Value at Risk)**: Perda potencial em cenário adverso
- **CVaR (Conditional VaR)**: Perda esperada dado que VaR foi excedido

---

## 🔧 CONFIGURAÇÕES PRINCIPAIS

### Arquivo: `config.json`

```json
{
  "nav": 1000000,                    // NAV inicial (R$ 1 milhão)
  "max_exposure": 0.5,               // Máximo 50% em posições
  "max_delta": 1000,                 // Limite de Delta
  "max_gamma": 500,                  // Limite de Gamma
  "max_vega": 1000,                  // Limite de Vega
  "kill_switch_threshold": 0.15,     // Kill switch em -15%
  
  "monitored_tickers": [             // 30 ações monitoradas
    "PETR4.SA", "VALE3.SA", ...     // 15 brasileiras
    "AAPL", "MSFT", ...              // 15 americanas
  ],
  
  "monitored_crypto": [              // 10 criptomoedas
    "BTC/USDT", "ETH/USDT", ...
  ],
  
  "enable_vol_arb": true,            // Ativar Vol Arb
  "enable_pairs": true,              // Ativar Pairs Trading
  "vol_arb_threshold": 0.08,         // Threshold para Vol Arb
  "pairs_zscore_threshold": 2.0,     // Z-score para Pairs
  
  "risk_free_rate": 0.05,            // Taxa livre de risco (5%)
  "commission_rate": 0.0002,         // Comissão (0.02%)
  "base_slippage": 0.0005            // Slippage base (0.05%)
}
```

---

## 🚀 COMO USAR O SISTEMA

### 1. Iniciar o Sistema

```bash
# Terminal 1: Iniciar API Server
python api_server.py

# Terminal 2: Iniciar Dashboard
streamlit run dashboard_central.py
```

### 2. Executar Backtest

**Via Dashboard:**
1. Abra o Dashboard em `http://localhost:8501`
2. Vá para aba "📈 Backtest"
3. Clique em "🔄 Executar Backtest"
4. Aguarde execução (pode levar alguns minutos)

**Via API:**
```bash
curl -X POST http://localhost:5000/backtest/run \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["PETR4.SA", "VALE3.SA"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "use_real_data": true
  }'
```

### 3. Monitorar Mercado em Tempo Real

1. No Dashboard, vá para aba "📝 Log de Monitoramento"
2. Clique em "▶️ Iniciar Monitoramento"
3. O sistema começará a escanear o mercado a cada 5 minutos
4. Oportunidades aparecerão na aba "📋 Ações Monitoradas"

### 4. Visualizar Resultados

- **Métricas**: Aba "📊 Visão Geral"
- **Trades**: Aba "🤖 Atividade dos Agentes"
- **Portfólio**: Aba "💰 Portfólio"
- **Logs**: Aba "📝 Log de Monitoramento"

---

## 📁 ESTRUTURA DE ARQUIVOS

```
algoritimo_trade_agentes/
├── api_server.py              # API REST Flask
├── dashboard_central.py        # Dashboard Streamlit
├── config.json                 # Configurações
│
├── src/
│   ├── agents.py              # TraderAgent, RiskAgent, PortfolioManager
│   ├── market_monitor.py      # 5 modelos de assimetria
│   ├── monitoring_service.py  # Serviço de monitoramento contínuo
│   ├── backtest.py            # Engine de backtest
│   ├── execution.py           # ExecutionSimulator
│   ├── pricing.py             # Black-Scholes e gregos
│   ├── data_loader.py         # Carregamento de dados
│   ├── market_data_api.py     # APIs de dados de mercado
│   ├── crypto_api.py          # API Binance (CCXT)
│   └── utils.py               # Utilitários e logging
│
├── output/                    # Resultados dos backtests
│   ├── metrics.csv
│   ├── portfolio_snapshots.csv
│   ├── orders.csv
│   └── fills.csv
│
└── logs/                      # Logs estruturados (JSON)
    └── *.jsonl
```

---

## 🔐 SEGURANÇA E CONTROLES

### Kill Switch

O RiskAgent possui um kill switch que para todas as operações se:
- Perda total > `kill_switch_threshold` (15% por padrão)
- NAV cai abaixo de 85% do inicial

### Limites de Risco

- **Por Ativo**: Máximo 5% do NAV por ativo
- **Total**: Máximo 50% do NAV em posições
- **Greeks**: Limites individuais para Delta, Gamma, Vega
- **Tamanho de Posição**: Máximo absoluto por ordem

### Logging

Todos os eventos são registrados em logs estruturados (JSON):
- Propostas do TraderAgent
- Avaliações do RiskAgent
- Execuções de ordens
- Oportunidades encontradas
- Erros e exceções

---

## 📧 PRÓXIMOS PASSOS

1. **Acesso Remoto**: Configurar túnel (ngrok/Cloudflare Tunnel) para acesso externo
2. **Alertas**: Implementar notificações por email/Telegram
3. **Broker Real**: Integrar com Interactive Brokers ou Binance
4. **Machine Learning**: Adicionar modelos preditivos
5. **Otimização**: Walk-forward optimization dos parâmetros

---

## 📞 SUPORTE

Para dúvidas ou problemas:
- Verifique os logs em `logs/`
- Consulte a documentação em `*.md`
- Execute testes: `python -m pytest tests/`

---

**Fim do Relatório**

