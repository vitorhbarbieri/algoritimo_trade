"""
Estratégia de tendência: cruzamento de médias móveis (SMA20 x SMA50)
"""
import pandas as pd
import numpy as np


def gerar_sinal_tendencia(df: pd.DataFrame) -> pd.Series:
    """
    Gera sinal baseado em cruzamento de médias móveis
    
    Sinais:
    +1: Compra (SMA20 cruza acima de SMA50)
    0: Neutro
    -1: Venda (SMA20 cruza abaixo de SMA50)
    
    Args:
        df: DataFrame com dados de preços e indicadores (deve ter SMA_20 e SMA_50)
    
    Returns:
        Series com sinais (+1, 0, -1)
    """
    sinais = pd.Series(0, index=df.index)
    
    if 'SMA_20' not in df.columns or 'SMA_50' not in df.columns:
        return sinais
    
    # Calcular cruzamentos
    sma20 = df['SMA_20']
    sma50 = df['SMA_50']
    
    # Sinal de compra: SMA20 cruza acima de SMA50
    cruzamento_cima = (sma20 > sma50) & (sma20.shift(1) <= sma50.shift(1))
    sinais[cruzamento_cima] = 1
    
    # Sinal de venda: SMA20 cruza abaixo de SMA50
    cruzamento_baixo = (sma20 < sma50) & (sma20.shift(1) >= sma50.shift(1))
    sinais[cruzamento_baixo] = -1
    
    return sinais


def gerar_sinal_tendencia_ema(df: pd.DataFrame) -> pd.Series:
    """
    Gera sinal baseado em cruzamento de EMAs (12 e 26)
    
    Args:
        df: DataFrame com dados de preços e indicadores (deve ter EMA_12 e EMA_26)
    
    Returns:
        Series com sinais (+1, 0, -1)
    """
    sinais = pd.Series(0, index=df.index)
    
    if 'EMA_12' not in df.columns or 'EMA_26' not in df.columns:
        return sinais
    
    ema12 = df['EMA_12']
    ema26 = df['EMA_26']
    
    # Compra: EMA12 cruza acima de EMA26
    cruzamento_cima = (ema12 > ema26) & (ema12.shift(1) <= ema26.shift(1))
    sinais[cruzamento_cima] = 1
    
    # Venda: EMA12 cruza abaixo de EMA26
    cruzamento_baixo = (ema12 < ema26) & (ema12.shift(1) >= ema26.shift(1))
    sinais[cruzamento_baixo] = -1
    
    return sinais


def calcular_forca_tendencia(df: pd.DataFrame) -> pd.Series:
    """
    Calcula força da tendência baseada em múltiplos fatores
    
    Args:
        df: DataFrame com indicadores
    
    Returns:
        Series com força da tendência (0 a 1)
    """
    forca = pd.Series(0.5, index=df.index)
    
    # Fator 1: Distância entre médias
    if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
        distancia = abs(df['SMA_20'] - df['SMA_50']) / df['SMA_50']
        forca += distancia * 0.3
    
    # Fator 2: RSI
    if 'RSI' in df.columns:
        rsi_normalizado = (df['RSI'] - 50) / 50  # Normalizar para -1 a 1
        forca += abs(rsi_normalizado) * 0.2
    
    # Limitar entre 0 e 1
    forca = forca.clip(0, 1)
    
    return forca


if __name__ == "__main__":
    # Teste
    print("Testando estratégia de tendência...")
    
    import yfinance as yf
    from features.technical_indicators import calcular_todos_indicadores
    
    dados = yf.download("ITUB4.SA", period="6mo", progress=False)
    
    if not dados.empty:
        df = calcular_todos_indicadores(dados)
        sinais = gerar_sinal_tendencia(df)
        
        print(f"\nSinais gerados:")
        print(f"Compras: {(sinais == 1).sum()}")
        print(f"Vendas: {(sinais == -1).sum()}")
        print(f"\nÚltimos sinais:")
        print(sinais.tail(10))









