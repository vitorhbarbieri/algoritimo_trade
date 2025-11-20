# 🚀 Algoritimo Trade

Sistema completo de trading algorítmico modular com múltiplos agentes e estratégias.

## 📁 Estrutura do Projeto

```
algoritimo_trade/
├── data/              # Coleta de dados
│   ├── price_collector.py
│   ├── news_collector.py
│   └── preprocess.py
├── features/          # Geração de features
│   ├── technical_indicators.py
│   ├── statistical_features.py
│   └── sentiment_engine.py
├── strategies/        # Estratégias de trading
│   ├── trend_strategy.py
│   ├── mean_reversion_strategy.py
│   └── news_strategy.py
├── core/             # Núcleo do sistema
│   ├── signal_orchestrator.py
│   ├── risk_manager.py
│   └── trade_executor.py
├── backtest/         # Backtesting
│   └── backtester.py
├── utils/            # Utilitários
│   ├── config.py
│   └── logger.py
├── main.py           # Pipeline principal
└── requirements.txt
```

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Executar pipeline completo:

```bash
python main.py ITUB4.SA
```

### Executar sem especificar ticker (usa padrão):

```bash
python main.py
```

## 🎯 Funcionalidades

- ✅ Coleta de dados de preços (yfinance)
- ✅ Coleta de notícias (web scraping)
- ✅ Indicadores técnicos (RSI, MACD, Bollinger, Médias Móveis)
- ✅ Features estatísticas (volatilidade, Z-score, momentum)
- ✅ Análise de sentimento de notícias
- ✅ Estratégias múltiplas (tendência, reversão, notícias)
- ✅ Orquestração de sinais com pesos configuráveis
- ✅ Gestão de risco (stop-loss, take-profit, tamanho de posição)
- ✅ Executor de trades (mock, preparado para APIs reais)
- ✅ Backtesting completo

## ⚙️ Configuração

Edite `utils/config.py` para ajustar:
- Tickers para operar
- Pesos das estratégias
- Limites de risco
- Parâmetros de indicadores

## 📊 Pipeline

1. **Coleta**: Preços + Notícias
2. **Preprocessamento**: Limpeza e merge
3. **Features**: Indicadores técnicos + estatísticos + sentimento
4. **Estratégias**: Geração de sinais individuais
5. **Orquestração**: Combinação de sinais
6. **Risk Manager**: Cálculo de stop-loss/take-profit
7. **Execução**: Simulação de trades

## 🌐 Deploy e GitHub

### 📦 GitHub

O projeto está configurado para GitHub. Para configurar:

1. **Siga o guia:** `GITHUB_SETUP.md`
2. **Ou execute:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/SEU_USUARIO/algoritimo-trade.git
   git push -u origin main
   ```

### 🚀 Deploy em Produção

O projeto está pronto para deploy em:
- **Railway** (recomendado - mais fácil)
- **Render** (gratuito)
- **Fly.io** (rápido)
- **Heroku** (pago)

**Guia completo:** `DEPLOY.md`

### 🔄 Atualizar Código

Use o script PowerShell para facilitar:
```powershell
.\git_push.ps1 "Descrição das mudanças"
```

Ou manualmente:
```bash
git add .
git commit -m "Descrição"
git push
```

## 🔧 Próximos Passos

- [x] Sistema de fallback para APIs de dividendos
- [x] Configuração para GitHub e deploy
- [ ] Integração com APIs de corretoras
- [ ] Machine Learning para otimização de pesos
- [x] Dashboard web
- [ ] Execução em tempo real
- [ ] Múltiplos timeframes simultâneos





