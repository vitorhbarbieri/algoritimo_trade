"""
Indicadores técnicos: RSI, MACD, Bollinger Bands, Médias Móveis
"""
import pandas as pd
import numpy as np


def calcular_rsi(df: pd.DataFrame, periodo: int = 14, coluna: str = 'Close') -> pd.Series:
    """
    Calcula o RSI (Relative Strength Index)
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período para cálculo (padrão: 14)
        coluna: Coluna de preço para usar
    
    Returns:
        Series com valores de RSI (0-100)
    """
    delta = df[coluna].diff()
    
    ganho = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    
    rs = ganho / perda
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calcular_macd(
    df: pd.DataFrame,
    rapida: int = 12,
    lenta: int = 26,
    sinal: int = 9,
    coluna: str = 'Close'
) -> pd.DataFrame:
    """
    Calcula o MACD (Moving Average Convergence Divergence)
    
    Args:
        df: DataFrame com dados de preços
        rapida: Período da média rápida
        lenta: Período da média lenta
        sinal: Período da linha de sinal
        coluna: Coluna de preço para usar
    
    Returns:
        DataFrame com MACD, Signal e Histogram
    """
    ema_rapida = df[coluna].ewm(span=rapida, adjust=False).mean()
    ema_lenta = df[coluna].ewm(span=lenta, adjust=False).mean()
    
    macd = ema_rapida - ema_lenta
    signal = macd.ewm(span=sinal, adjust=False).mean()
    histogram = macd - signal
    
    resultado = pd.DataFrame({
        'MACD': macd,
        'Signal': signal,
        'Histogram': histogram
    })
    
    return resultado


def calcular_bollinger_bands(
    df: pd.DataFrame,
    periodo: int = 20,
    desvio: float = 2.0,
    coluna: str = 'Close'
) -> pd.DataFrame:
    """
    Calcula as Bandas de Bollinger
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período da média móvel
        desvio: Número de desvios padrão
        coluna: Coluna de preço para usar
    
    Returns:
        DataFrame com Upper, Middle (SMA) e Lower bands
    """
    sma = df[coluna].rolling(window=periodo).mean()
    std = df[coluna].rolling(window=periodo).std()
    
    upper = sma + (std * desvio)
    lower = sma - (std * desvio)
    
    resultado = pd.DataFrame({
        'BB_Upper': upper,
        'BB_Middle': sma,
        'BB_Lower': lower
    })
    
    return resultado


def calcular_sma(df: pd.DataFrame, periodo: int, coluna: str = 'Close') -> pd.Series:
    """
    Calcula Média Móvel Simples (SMA)
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período da média
        coluna: Coluna de preço para usar
    
    Returns:
        Series com valores da SMA
    """
    return df[coluna].rolling(window=periodo).mean()


def calcular_ema(df: pd.DataFrame, periodo: int, coluna: str = 'Close') -> pd.Series:
    """
    Calcula Média Móvel Exponencial (EMA)
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período da média
        coluna: Coluna de preço para usar
    
    Returns:
        Series com valores da EMA
    """
    return df[coluna].ewm(span=periodo, adjust=False).mean()


def calcular_atr(df: pd.DataFrame, periodo: int = 14) -> pd.Series:
    """
    Calcula o ATR (Average True Range) para stop-loss
    
    Args:
        df: DataFrame com dados OHLC
        periodo: Período para cálculo
    
    Returns:
        Series com valores de ATR
    """
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=periodo).mean()
    
    return atr


def calcular_todos_indicadores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula todos os indicadores técnicos e adiciona ao DataFrame
    
    Args:
        df: DataFrame com dados OHLCV
    
    Returns:
        DataFrame original com colunas de indicadores adicionadas
    """
    df = df.copy()
    
    # RSI
    df['RSI'] = calcular_rsi(df)
    
    # MACD
    macd_data = calcular_macd(df)
    df = pd.concat([df, macd_data], axis=1)
    
    # Bollinger Bands
    bb_data = calcular_bollinger_bands(df)
    df = pd.concat([df, bb_data], axis=1)
    
    # Médias móveis
    df['SMA_20'] = calcular_sma(df, 20)
    df['SMA_50'] = calcular_sma(df, 50)
    df['EMA_12'] = calcular_ema(df, 12)
    df['EMA_26'] = calcular_ema(df, 26)
    
    # ATR
    df['ATR'] = calcular_atr(df)
    
    return df


if __name__ == "__main__":
    # Teste
    print("Testando indicadores técnicos...")
    
    import yfinance as yf
    dados = yf.download("ITUB4.SA", period="3mo", progress=False)
    
    if not dados.empty:
        df_com_indicadores = calcular_todos_indicadores(dados)
        print(f"\nIndicadores calculados:")
        print(df_com_indicadores[['Close', 'RSI', 'MACD', 'BB_Upper', 'SMA_20', 'ATR']].tail())






