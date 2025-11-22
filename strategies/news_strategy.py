"""
Estratégia baseada em notícias e sentimento
Compra se sentimento > 0.4, vende se sentimento < -0.4
"""
import pandas as pd
from features.sentiment_engine import analisar_sentimento_noticias
from typing import List, Dict


def gerar_sinal_noticias(
    noticias: List[Dict],
    threshold_positivo: float = 0.4,
    threshold_negativo: float = -0.4
) -> float:
    """
    Gera sinal baseado em sentimento das notícias
    
    Sinais:
    +1: Compra (sentimento > threshold_positivo)
    0: Neutro
    -1: Venda (sentimento < threshold_negativo)
    
    Args:
        noticias: Lista de notícias
        threshold_positivo: Limiar para sinal de compra
        threshold_negativo: Limiar para sinal de venda
    
    Returns:
        Sinal (-1, 0, ou +1)
    """
    if not noticias:
        return 0.0
    
    sentimento = analisar_sentimento_noticias(noticias)
    
    if sentimento > threshold_positivo:
        return 1.0
    elif sentimento < threshold_negativo:
        return -1.0
    else:
        return 0.0


def gerar_sinal_noticias_por_periodo(
    df: pd.DataFrame,
    noticias_por_data: Dict,
    threshold_positivo: float = 0.4,
    threshold_negativo: float = -0.4
) -> pd.Series:
    """
    Gera sinais de notícias para cada período do DataFrame
    
    Args:
        df: DataFrame com índice de datas
        noticias_por_data: Dicionário {data: [notícias]}
        threshold_positivo: Limiar para compra
        threshold_negativo: Limiar para venda
    
    Returns:
        Series com sinais por data
    """
    sinais = pd.Series(0.0, index=df.index)
    
    for data in df.index:
        data_str = data.strftime('%Y-%m-%d')
        if data_str in noticias_por_data:
            noticias = noticias_por_data[data_str]
            sinal = gerar_sinal_noticias(noticias, threshold_positivo, threshold_negativo)
            sinais[data] = sinal
    
    return sinais


def calcular_forca_sentimento(noticias: List[Dict]) -> float:
    """
    Calcula força do sentimento (magnitude, não direção)
    
    Args:
        noticias: Lista de notícias
    
    Returns:
        Força do sentimento (0 a 1)
    """
    if not noticias:
        return 0.0
    
    sentimento = analisar_sentimento_noticias(noticias)
    
    # Força é a magnitude absoluta
    forca = abs(sentimento)
    
    return forca


def combinar_sentimento_volume(
    sentimento: float,
    num_noticias: int,
    threshold_noticias: int = 5
) -> float:
    """
    Combina sentimento com volume de notícias
    
    Se houver poucas notícias, reduz a confiança no sinal
    
    Args:
        sentimento: Score de sentimento
        num_noticias: Número de notícias
        threshold_noticias: Número mínimo de notícias para confiança total
    
    Returns:
        Sinal ajustado pela confiança
    """
    if num_noticias < threshold_noticias:
        # Reduzir magnitude do sinal se poucas notícias
        fator_confianca = num_noticias / threshold_noticias
        return sentimento * fator_confianca
    
    return sentimento


if __name__ == "__main__":
    # Teste
    print("Testando estratégia de notícias...")
    
    noticias_teste = [
        {'titulo': 'Itaú registra lucro recorde e ações sobem', 'resumo': 'Bom resultado'},
        {'titulo': 'Bancos têm crescimento forte no trimestre', 'resumo': 'Setor em alta'},
        {'titulo': 'Confiança do mercado aumenta', 'resumo': 'Perspectivas positivas'}
    ]
    
    sinal = gerar_sinal_noticias(noticias_teste)
    forca = calcular_forca_sentimento(noticias_teste)
    
    print(f"\nNotícias: {len(noticias_teste)}")
    print(f"Sinal: {sinal:+.1f}")
    print(f"Força: {forca:.3f}")









