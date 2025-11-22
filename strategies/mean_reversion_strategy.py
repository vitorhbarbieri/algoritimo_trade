"""
Estratégia de reversão à média: Z-score
Compra quando preço está muito abaixo da média, vende quando muito acima
"""
import pandas as pd
import numpy as np


def gerar_sinal_reversao(df: pd.DataFrame, zscore_threshold: float = 2.0) -> pd.Series:
    """
    Gera sinal baseado em reversão à média usando Z-score
    
    Sinais:
    +1: Compra (Z-score < -threshold, preço muito abaixo da média)
    0: Neutro
    -1: Venda (Z-score > threshold, preço muito acima da média)
    
    Args:
        df: DataFrame com dados de preços e ZScore
        zscore_threshold: Limiar de Z-score para gerar sinal (padrão: 2.0)
    
    Returns:
        Series com sinais (+1, 0, -1)
    """
    sinais = pd.Series(0, index=df.index)
    
    if 'ZScore' not in df.columns:
        return sinais
    
    zscore = df['ZScore']
    
    # Compra: Z-score muito negativo (preço muito abaixo da média)
    sinais[zscore < -zscore_threshold] = 1
    
    # Venda: Z-score muito positivo (preço muito acima da média)
    sinais[zscore > zscore_threshold] = -1
    
    return sinais


def gerar_sinal_bollinger_reversao(df: pd.DataFrame) -> pd.Series:
    """
    Gera sinal baseado em reversão usando Bandas de Bollinger
    
    Compra quando preço toca banda inferior
    Vende quando preço toca banda superior
    
    Args:
        df: DataFrame com dados de preços e Bandas de Bollinger
    
    Returns:
        Series com sinais (+1, 0, -1)
    """
    sinais = pd.Series(0, index=df.index)
    
    if 'BB_Upper' not in df.columns or 'BB_Lower' not in df.columns or 'Close' not in df.columns:
        return sinais
    
    preco = df['Close']
    bb_upper = df['BB_Upper']
    bb_lower = df['BB_Lower']
    
    # Compra: preço toca ou fica abaixo da banda inferior
    sinais[preco <= bb_lower] = 1
    
    # Venda: preço toca ou fica acima da banda superior
    sinais[preco >= bb_upper] = -1
    
    return sinais


def calcular_probabilidade_reversao(df: pd.DataFrame) -> pd.Series:
    """
    Calcula probabilidade de reversão baseada em Z-score
    
    Args:
        df: DataFrame com ZScore
    
    Returns:
        Series com probabilidade (0 a 1)
    """
    probabilidade = pd.Series(0.5, index=df.index)
    
    if 'ZScore' not in df.columns:
        return probabilidade
    
    zscore = df['ZScore']
    
    # Quanto mais extremo o Z-score, maior a probabilidade de reversão
    zscore_abs = abs(zscore)
    
    # Normalizar para 0-1 (assumindo que Z-score > 3 é muito raro)
    probabilidade = np.clip(zscore_abs / 3.0, 0, 1)
    
    return probabilidade


if __name__ == "__main__":
    # Teste
    print("Testando estratégia de reversão à média...")
    
    import yfinance as yf
    from features.technical_indicators import calcular_todos_indicadores
    from features.statistical_features import calcular_todas_features_estatisticas
    
    dados = yf.download("ITUB4.SA", period="6mo", progress=False)
    
    if not dados.empty:
        df = calcular_todos_indicadores(dados)
        df = calcular_todas_features_estatisticas(df)
        
        sinais = gerar_sinal_reversao(df)
        
        print(f"\nSinais gerados:")
        print(f"Compras: {(sinais == 1).sum()}")
        print(f"Vendas: {(sinais == -1).sum()}")
        print(f"\nÚltimos sinais:")
        print(sinais.tail(10))










