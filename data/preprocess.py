"""
Preprocessamento e limpeza de dados
Merge de preços e notícias por timestamp
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional


def limpar_dados_precos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza dados de preços
    
    Args:
        df: DataFrame com dados OHLCV
    
    Returns:
        DataFrame limpo
    """
    df = df.copy()
    
    # Remover linhas com valores NaN
    df = df.dropna()
    
    # Remover valores negativos ou zero
    for col in ['Open', 'High', 'Low', 'Close']:
        df = df[df[col] > 0]
    
    # Garantir que High >= Low
    df = df[df['High'] >= df['Low']]
    
    # Garantir que Close está entre Low e High
    df = df[(df['Close'] >= df['Low']) & (df['Close'] <= df['High'])]
    
    # Remover duplicatas
    df = df[~df.index.duplicated(keep='first')]
    
    # Ordenar por data
    df = df.sort_index()
    
    return df


def padronizar_noticias(noticias: List[Dict]) -> pd.DataFrame:
    """
    Converte lista de notícias em DataFrame padronizado
    
    Args:
        noticias: Lista de dicionários com notícias
    
    Returns:
        DataFrame com notícias padronizadas
    """
    if not noticias:
        return pd.DataFrame()
    
    df = pd.DataFrame(noticias)
    
    # Converter timestamp para datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
        df['timestamp'] = pd.to_datetime(df.get('data', datetime.now()))
    
    # Garantir colunas necessárias
    colunas_necessarias = ['titulo', 'resumo', 'link', 'fonte', 'timestamp']
    for col in colunas_necessarias:
        if col not in df.columns:
            df[col] = ''
    
    # Remover duplicatas por título
    df = df.drop_duplicates(subset=['titulo'], keep='first')
    
    # Ordenar por timestamp
    df = df.sort_values('timestamp')
    
    return df[colunas_necessarias]


def merge_precos_noticias(
    df_precos: pd.DataFrame,
    df_noticias: pd.DataFrame,
    janela_horaria: str = '1H'
) -> pd.DataFrame:
    """
    Faz merge de preços e notícias por timestamp
    
    Args:
        df_precos: DataFrame com dados de preços
        df_noticias: DataFrame com notícias
        janela_horaria: Janela para agrupar notícias (ex: '1H', '1D')
    
    Returns:
        DataFrame com preços e contagem de notícias por período
    """
    if df_noticias.empty:
        df_precos['num_noticias'] = 0
        return df_precos
    
    # Agrupar notícias por janela horária
    df_noticias['periodo'] = df_noticias['timestamp'].dt.floor(janela_horaria)
    noticias_agrupadas = df_noticias.groupby('periodo').size().reset_index(name='num_noticias')
    
    # Fazer merge com preços
    df_precos['periodo'] = df_precos.index.floor(janela_horaria)
    df_merged = df_precos.merge(
        noticias_agrupadas,
        on='periodo',
        how='left'
    )
    
    # Preencher NaN com 0
    df_merged['num_noticias'] = df_merged['num_noticias'].fillna(0).astype(int)
    
    # Remover coluna auxiliar
    df_merged = df_merged.drop('periodo', axis=1)
    
    return df_merged


def preparar_dados_completos(
    df_precos: pd.DataFrame,
    noticias: List[Dict],
    janela_horaria: str = '1D'
) -> pd.DataFrame:
    """
    Pipeline completo de preparação de dados
    
    Args:
        df_precos: DataFrame com preços
        noticias: Lista de notícias
        janela_horaria: Janela para agrupar
    
    Returns:
        DataFrame final preparado
    """
    # Limpar preços
    df_precos_limpo = limpar_dados_precos(df_precos)
    
    # Padronizar notícias
    df_noticias = padronizar_noticias(noticias)
    
    # Merge
    df_final = merge_precos_noticias(df_precos_limpo, df_noticias, janela_horaria)
    
    return df_final


if __name__ == "__main__":
    # Teste
    print("Testando preprocessamento...")
    
    # Dados de exemplo
    dates = pd.date_range('2025-01-01', periods=10, freq='D')
    df_precos = pd.DataFrame({
        'Open': np.random.uniform(20, 25, 10),
        'High': np.random.uniform(25, 30, 10),
        'Low': np.random.uniform(15, 20, 10),
        'Close': np.random.uniform(20, 25, 10),
        'Volume': np.random.randint(1000000, 5000000, 10)
    }, index=dates)
    
    noticias = [
        {'titulo': 'Notícia 1', 'resumo': 'Resumo 1', 'link': 'link1', 
         'fonte': 'g1', 'timestamp': datetime(2025, 1, 2)},
        {'titulo': 'Notícia 2', 'resumo': 'Resumo 2', 'link': 'link2',
         'fonte': 'valor', 'timestamp': datetime(2025, 1, 3)}
    ]
    
    df_final = preparar_dados_completos(df_precos, noticias)
    print(f"\nDados preparados:")
    print(df_final.head())










