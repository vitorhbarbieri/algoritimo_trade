"""
Engine de análise de sentimento
Usa Vader ou TextBlob para gerar score de -1 a +1
"""
from textblob import TextBlob
import re
from typing import List, Dict


# Dicionário de palavras positivas e negativas em português
PALAVRAS_POSITIVAS = {
    'alta', 'subiu', 'cresceu', 'lucro', 'ganho', 'bom', 'ótimo', 'excelente',
    'positivo', 'forte', 'melhor', 'melhora', 'aumento', 'crescimento',
    'expansão', 'sucesso', 'recorde', 'superou', 'superação', 'otimista',
    'confiança', 'investimento', 'oportunidade', 'valorização', 'apreciação',
    'boom', 'pujante', 'robusto', 'sólido', 'promissor', 'alta', 'sobe'
}

PALAVRAS_NEGATIVAS = {
    'queda', 'caiu', 'perda', 'prejuízo', 'ruim', 'péssimo', 'negativo',
    'fraco', 'pior', 'piora', 'declínio', 'recessão', 'crise',
    'falência', 'dívida', 'risco', 'incerteza', 'pessimista', 'desconfiança',
    'desvalorização', 'baixa', 'depreciação', 'crash', 'colapso', 'frágil',
    'instável', 'preocupante', 'alerta', 'tensão', 'conflito', 'problema', 'cai'
}


def analisar_sentimento_lexico(texto: str) -> float:
    """
    Analisa sentimento usando dicionário léxico em português
    
    Args:
        texto: Texto para analisar
    
    Returns:
        Score de -1 (muito negativo) a +1 (muito positivo)
    """
    texto_lower = texto.lower()
    palavras = texto_lower.split()
    
    # Contar palavras positivas e negativas
    positivas_count = sum(1 for palavra in palavras if palavra in PALAVRAS_POSITIVAS)
    negativas_count = sum(1 for palavra in palavras if palavra in PALAVRAS_NEGATIVAS)
    
    # Calcular score
    total_palavras_sentimento = positivas_count + negativas_count
    if total_palavras_sentimento == 0:
        return 0.0
    
    diferenca = positivas_count - negativas_count
    score = diferenca / max(total_palavras_sentimento, 1)
    
    # Limitar entre -1 e 1
    return max(-1.0, min(1.0, score))


def analisar_sentimento_textblob(texto: str) -> float:
    """
    Analisa sentimento usando TextBlob (funciona melhor com inglês)
    
    Args:
        texto: Texto para analisar
    
    Returns:
        Score de -1 a +1
    """
    try:
        blob = TextBlob(texto)
        return blob.sentiment.polarity
    except:
        return 0.0


def analisar_sentimento(texto: str, metodo: str = 'lexico') -> float:
    """
    Analisa sentimento de um texto
    
    Args:
        texto: Texto para analisar
        metodo: 'lexico' (português) ou 'textblob' (inglês)
    
    Returns:
        Score de -1 a +1
    """
    if metodo == 'lexico':
        return analisar_sentimento_lexico(texto)
    else:
        return analisar_sentimento_textblob(texto)


def analisar_sentimento_noticias(noticias: List[Dict]) -> float:
    """
    Analisa sentimento agregado de uma lista de notícias
    
    Args:
        noticias: Lista de dicionários com notícias (deve ter 'titulo' e 'resumo')
    
    Returns:
        Score médio de sentimento (-1 a +1)
    """
    if not noticias:
        return 0.0
    
    sentimentos = []
    for noticia in noticias:
        texto = f"{noticia.get('titulo', '')} {noticia.get('resumo', '')}"
        sentimento = analisar_sentimento(texto)
        sentimentos.append(sentimento)
    
    return sum(sentimentos) / len(sentimentos) if sentimentos else 0.0


def classificar_sentimento(score: float) -> str:
    """
    Classifica o score de sentimento em categoria
    
    Args:
        score: Score de sentimento (-1 a +1)
    
    Returns:
        'muito_positivo', 'positivo', 'neutro', 'negativo', 'muito_negativo'
    """
    if score > 0.4:
        return 'muito_positivo'
    elif score > 0.1:
        return 'positivo'
    elif score < -0.4:
        return 'muito_negativo'
    elif score < -0.1:
        return 'negativo'
    else:
        return 'neutro'


if __name__ == "__main__":
    # Teste
    print("Testando engine de sentimento...")
    
    textos_teste = [
        "Itaú registra lucro recorde e ações sobem no mercado",
        "Petrobras enfrenta crise e ações caem drasticamente",
        "Banco Central mantém taxa de juros estável"
    ]
    
    for texto in textos_teste:
        score = analisar_sentimento(texto)
        classificacao = classificar_sentimento(score)
        print(f"\nTexto: {texto[:50]}...")
        print(f"Score: {score:+.3f} | Classificação: {classificacao}")









