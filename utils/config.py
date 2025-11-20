"""
Configurações do sistema: tickers, timeframes, pesos das estratégias, limites de risco
"""
from typing import Dict, List


# Tickers para operar
TICKERS = [
    'BBSE3.SA',  # Banco do Brasil
    'CMIG4.SA',  # Cemig
    'CSMG3.SA',  # Copasa
    'ITUB4.SA',  # Itaú
    'PETR4.SA',  # Petrobras
    'SANB11.SA', # Santander
    'SYN3.SA'    # SYN
]

# Timeframes disponíveis
TIMEFRAMES = {
    '1m': '1m',
    '5m': '5m',
    '15m': '15m',
    '1h': '1h',
    '1d': '1d'
}

# Período padrão para coleta de dados
PERIODO_PADRAO = '6mo'

# Pesos das estratégias no orquestrador
PESOS_ESTRATEGIAS = {
    'trend': 0.4,      # 40% peso para estratégia de tendência
    'reversao': 0.3,   # 30% peso para estratégia de reversão
    'news': 0.3        # 30% peso para estratégia de notícias
}

# Limites de risco
RISCO_POR_TRADE = 0.02  # 2% da banca por trade
MAX_POSICAO = 0.1       # Máximo 10% da banca em uma posição
STOP_LOSS_ATR_MULTIPLIER = 2.0
TAKE_PROFIT_ATR_MULTIPLIER = 3.0

# Configurações de indicadores técnicos
RSI_PERIODO = 14
MACD_RAPIDA = 12
MACD_LENTA = 26
MACD_SINAL = 9
BOLLINGER_PERIODO = 20
BOLLINGER_DESVIO = 2.0
SMA_PERIODOS = [20, 50]
EMA_PERIODOS = [12, 26]

# Configurações de features estatísticas
VOLATILIDADE_PERIODO = 20
ZSCORE_PERIODO = 20
MOMENTUM_PERIODOS = [10, 20]

# Configurações de sentimento
SENTIMENTO_THRESHOLD_POSITIVO = 0.4
SENTIMENTO_THRESHOLD_NEGATIVO = -0.4
SENTIMENTO_METODO = 'lexico'  # 'lexico' ou 'textblob'

# Configurações de reversão
ZSCORE_THRESHOLD = 2.0

# Configurações de backtest
CAPITAL_INICIAL = 10000.0

# Sites de notícias
SITES_NOTICIAS = ['g1', 'valor', 'folha']

# Configurações de logging
LOG_LEVEL = 'INFO'  # 'DEBUG', 'INFO', 'WARNING', 'ERROR'

