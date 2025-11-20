"""
Features estatísticas: volatilidade, retorno log, Z-score, correlações
"""
import pandas as pd
import numpy as np


def calcular_volatilidade(df: pd.DataFrame, periodo: int = 20, coluna: str = 'Close') -> pd.Series:
    """
    Calcula a volatilidade (desvio padrão dos retornos)
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período para cálculo
        coluna: Coluna de preço para usar
    
    Returns:
        Series com valores de volatilidade
    """
    retornos = df[coluna].pct_change()
    volatilidade = retornos.rolling(window=periodo).std() * np.sqrt(252)  # Anualizada
    return volatilidade


def calcular_retorno_log(df: pd.DataFrame, coluna: str = 'Close') -> pd.Series:
    """
    Calcula o retorno logarítmico
    
    Args:
        df: DataFrame com dados de preços
        coluna: Coluna de preço para usar
    
    Returns:
        Series com retornos log
    """
    return np.log(df[coluna] / df[coluna].shift(1))


def calcular_zscore(df: pd.DataFrame, periodo: int = 20, coluna: str = 'Close') -> pd.Series:
    """
    Calcula o Z-score (quantos desvios padrão do preço está da média)
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período para cálculo da média e desvio
        coluna: Coluna de preço para usar
    
    Returns:
        Series com valores de Z-score
    """
    media = df[coluna].rolling(window=periodo).mean()
    std = df[coluna].rolling(window=periodo).std()
    zscore = (df[coluna] - media) / std
    return zscore


def calcular_correlacao_retornos(df1: pd.Series, df2: pd.Series, periodo: int = 20) -> pd.Series:
    """
    Calcula correlação móvel entre duas séries de retornos
    
    Args:
        df1: Primeira série de preços
        df2: Segunda série de preços
        periodo: Período para cálculo da correlação
    
    Returns:
        Series com valores de correlação (-1 a 1)
    """
    retornos1 = df1.pct_change()
    retornos2 = df2.pct_change()
    
    correlacao = retornos1.rolling(window=periodo).corr(retornos2)
    return correlacao


def calcular_momentum(df: pd.DataFrame, periodo: int = 10, coluna: str = 'Close') -> pd.Series:
    """
    Calcula o momentum (variação percentual em N períodos)
    
    Args:
        df: DataFrame com dados de preços
        periodo: Período para cálculo
        coluna: Coluna de preço para usar
    
    Returns:
        Series com valores de momentum
    """
    return df[coluna].pct_change(periods=periodo)


def calcular_todas_features_estatisticas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula todas as features estatísticas e adiciona ao DataFrame
    
    Args:
        df: DataFrame com dados de preços
    
    Returns:
        DataFrame original com features adicionadas
    """
    df = df.copy()
    
    # Volatilidade
    df['Volatilidade'] = calcular_volatilidade(df)
    
    # Retorno log
    df['Retorno_Log'] = calcular_retorno_log(df)
    
    # Z-score
    df['ZScore'] = calcular_zscore(df)
    
    # Momentum
    df['Momentum_10'] = calcular_momentum(df, 10)
    df['Momentum_20'] = calcular_momentum(df, 20)
    
    return df


if __name__ == "__main__":
    # Teste
    print("Testando features estatísticas...")
    
    import yfinance as yf
    dados = yf.download("ITUB4.SA", period="3mo", progress=False)
    
    if not dados.empty:
        df_com_features = calcular_todas_features_estatisticas(dados)
        print(f"\nFeatures calculadas:")
        print(df_com_features[['Close', 'Volatilidade', 'ZScore', 'Momentum_10']].tail())






