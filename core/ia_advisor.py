"""
Módulo de análise de IA para recomendar movimentos estratégicos na carteira.
Suporta múltiplos provedores de IA (OpenAI, Claude, etc.)
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def analisar_carteira_com_ia(
    positions: List[Dict[str, Any]],
    pnl_carteira: float,
    pnl_realizado: float,
    pnl_total: float,
    rentabilidade_carteira: float,
    rentabilidade_realizada: float,
    rentabilidade_total: float,
    total_investido: float,
    total_valor: float,
    custo_vendas: float,
    receita_vendas: float
) -> Dict[str, Any]:
    """
    Analisa a carteira usando IA e retorna recomendações estratégicas.
    
    Args:
        positions: Lista de posições com ticker, quantidade, preço médio, preço último, rentabilidade
        pnl_carteira: PnL não realizado (posições abertas)
        pnl_realizado: PnL realizado (vendas)
        pnl_total: PnL total
        rentabilidade_carteira: Rentabilidade das posições abertas
        rentabilidade_realizada: Rentabilidade das vendas
        rentabilidade_total: Rentabilidade total
        total_investido: Total investido em posições abertas
        total_valor: Valor atual das posições abertas
        custo_vendas: Custo das ações vendidas
        receita_vendas: Receita das vendas
    
    Returns:
        Dict com recomendações estruturadas da IA
    """
    try:
        # Formatar dados da carteira para o prompt
        carteira_texto = _formatar_carteira_para_prompt(
            positions, pnl_carteira, pnl_realizado, pnl_total,
            rentabilidade_carteira, rentabilidade_realizada, rentabilidade_total,
            total_investido, total_valor, custo_vendas, receita_vendas
        )
        
        # Gerar prompt estruturado
        prompt = _criar_prompt_analise(carteira_texto)
        
        # Chamar IA (tentar OpenAI primeiro, depois fallback)
        recomendacoes = _chamar_ia(prompt)
        
        return {
            "status": "ok",
            "recomendacoes": recomendacoes,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Erro ao analisar carteira com IA: {str(e)}")
        return {
            "status": "erro",
            "erro": str(e),
            "recomendacoes": _gerar_recomendacoes_fallback(positions),
            "timestamp": datetime.now().isoformat()
        }

def _formatar_carteira_para_prompt(
    positions: List[Dict[str, Any]],
    pnl_carteira: float,
    pnl_realizado: float,
    pnl_total: float,
    rentabilidade_carteira: float,
    rentabilidade_realizada: float,
    rentabilidade_total: float,
    total_investido: float,
    total_valor: float,
    custo_vendas: float,
    receita_vendas: float
) -> str:
    """Formata os dados da carteira em texto estruturado para o prompt."""
    texto = f"""CARTEIRA DE INVESTIMENTOS - ANÁLISE ESTRATÉGICA

RESUMO GERAL:
- Total Investido (Posições Abertas): R$ {total_investido:,.2f}
- Valor Atual (Posições Abertas): R$ {total_valor:,.2f}
- PnL Carteira (Não Realizado): R$ {pnl_carteira:,.2f} ({rentabilidade_carteira*100:.2f}%)
- PnL Realizado (Vendas): R$ {pnl_realizado:,.2f} ({rentabilidade_realizada*100:.2f}%)
- PnL Total: R$ {pnl_total:,.2f} ({rentabilidade_total*100:.2f}%)
- Custo das Vendas: R$ {custo_vendas:,.2f}
- Receita das Vendas: R$ {receita_vendas:,.2f}

POSIÇÕES ABERTAS:
"""
    for pos in positions:
        ticker = pos.get('ticker', 'N/A')
        qty = pos.get('quantidade', 0)
        preco_medio = pos.get('preco_medio', 0)
        preco_ultimo = pos.get('preco_ultimo')
        valor_posicao = pos.get('valor_posicao')
        rentabilidade = pos.get('rentabilidade')
        rentabilidade_anualizada = pos.get('rentabilidade_anualizada')
        
        texto += f"\n- {ticker}:\n"
        texto += f"  Quantidade: {qty}\n"
        texto += f"  Preço Médio: R$ {preco_medio:.2f}\n"
        if preco_ultimo:
            texto += f"  Preço Atual: R$ {preco_ultimo:.2f}\n"
            if valor_posicao:
                texto += f"  Valor da Posição: R$ {valor_posicao:,.2f}\n"
            if rentabilidade is not None:
                texto += f"  Rentabilidade: {rentabilidade*100:.2f}%\n"
            if rentabilidade_anualizada is not None:
                texto += f"  Rentabilidade Anualizada: {rentabilidade_anualizada*100:.2f}%\n"
        else:
            texto += f"  Preço Atual: Não disponível\n"
    
    return texto

def _criar_prompt_analise(carteira_texto: str) -> str:
    """Cria o prompt completo para análise da IA."""
    return f"""Você é um analista especializado em trading e gestão de carteiras de ações brasileiras (B3).

Analise a seguinte carteira e forneça recomendações estratégicas detalhadas:

{carteira_texto}

INSTRUÇÕES:
1. Analise o desempenho de cada posição
2. Identifique oportunidades de otimização
3. Sugira movimentos estratégicos (manter, aumentar, reduzir, vender)
4. Considere diversificação, concentração de risco e rentabilidade
5. Priorize ações com melhor perspectiva de valorização
6. Alerte sobre posições com risco elevado ou baixa rentabilidade

FORMATO DE RESPOSTA (JSON):
{{
  "resumo": "Resumo executivo da análise em 2-3 frases",
  "recomendacoes": [
    {{
      "ticker": "BBSE3",
      "acao": "MANTER|AUMENTAR|REDUZIR|VENDER",
      "justificativa": "Explicação detalhada da recomendação",
      "prioridade": "ALTA|MEDIA|BAIXA",
      "rentabilidade_atual": "X%",
      "perspectiva": "Boa perspectiva de valorização baseada em..."
    }}
  ],
  "observacoes_gerais": [
    "Observação 1 sobre a carteira",
    "Observação 2 sobre diversificação",
    "Observação 3 sobre risco"
  ],
  "sugestoes_estrategicas": [
    "Sugestão estratégica 1",
    "Sugestão estratégica 2"
  ]
}}

Responda APENAS com o JSON válido, sem texto adicional antes ou depois.
"""

def _chamar_ia(prompt: str) -> Dict[str, Any]:
    """Chama a API de IA (OpenAI, Claude, etc.)"""
    # Tentar OpenAI primeiro
    try:
        return _chamar_openai(prompt)
    except Exception as e_openai:
        logger.warning(f"⚠️  OpenAI falhou: {str(e_openai)[:100]}")
        # Tentar Claude se disponível
        try:
            return _chamar_claude(prompt)
        except Exception as e_claude:
            logger.warning(f"⚠️  Claude falhou: {str(e_claude)[:100]}")
            # Fallback para recomendações básicas
            raise Exception("Nenhuma API de IA disponível")

def _chamar_openai(prompt: str) -> Dict[str, Any]:
    """Chama a API da OpenAI (GPT-4 ou GPT-3.5-turbo)"""
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Você é um analista especializado em trading e gestão de carteiras. Sempre responda em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        resposta_texto = response.choices[0].message.content.strip()
        
        # Tentar extrair JSON da resposta
        json_texto = _extrair_json_da_resposta(resposta_texto)
        return json.loads(json_texto)
        
    except ImportError:
        raise Exception("Biblioteca openai não instalada. Execute: pip install openai")
    except Exception as e:
        raise Exception(f"Erro ao chamar OpenAI: {str(e)}")

def _chamar_claude(prompt: str) -> Dict[str, Any]:
    """Chama a API da Anthropic (Claude)"""
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        
        client = Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        resposta_texto = response.content[0].text.strip()
        json_texto = _extrair_json_da_resposta(resposta_texto)
        return json.loads(json_texto)
        
    except ImportError:
        raise Exception("Biblioteca anthropic não instalada. Execute: pip install anthropic")
    except Exception as e:
        raise Exception(f"Erro ao chamar Claude: {str(e)}")

def _extrair_json_da_resposta(texto: str) -> str:
    """Extrai JSON de uma resposta que pode conter texto antes/depois."""
    # Tentar encontrar JSON entre chaves
    inicio = texto.find('{')
    fim = texto.rfind('}') + 1
    
    if inicio >= 0 and fim > inicio:
        return texto[inicio:fim]
    
    # Se não encontrar, retornar o texto original
    return texto

def _gerar_recomendacoes_fallback(positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gera recomendações básicas quando a IA não está disponível."""
    recomendacoes = []
    
    for pos in positions:
        ticker = pos.get('ticker', 'N/A')
        rentabilidade = pos.get('rentabilidade')
        rentabilidade_anualizada = pos.get('rentabilidade_anualizada')
        
        if rentabilidade is None:
            acao = "ANALISAR"
            justificativa = "Preço não disponível. Verifique se o ticker está correto."
            prioridade = "MEDIA"
        elif rentabilidade < -0.1:  # -10%
            acao = "REDUZIR"
            justificativa = f"Rentabilidade negativa de {rentabilidade*100:.2f}%. Considere reduzir exposição."
            prioridade = "ALTA"
        elif rentabilidade > 0.2:  # +20%
            acao = "MANTER"
            justificativa = f"Boa rentabilidade de {rentabilidade*100:.2f}%. Mantenha a posição."
            prioridade = "MEDIA"
        else:
            acao = "MANTER"
            justificativa = f"Rentabilidade de {rentabilidade*100:.2f}%. Monitore a evolução."
            prioridade = "BAIXA"
        
        recomendacoes.append({
            "ticker": ticker,
            "acao": acao,
            "justificativa": justificativa,
            "prioridade": prioridade,
            "rentabilidade_atual": f"{rentabilidade*100:.2f}%" if rentabilidade else "N/A"
        })
    
    return {
        "resumo": "Análise básica baseada em rentabilidade. Para recomendações mais detalhadas, configure uma API de IA (OpenAI ou Claude).",
        "recomendacoes": recomendacoes,
        "observacoes_gerais": [
            "Recomendações geradas automaticamente baseadas em rentabilidade.",
            "Configure OPENAI_API_KEY ou ANTHROPIC_API_KEY para análises mais profundas."
        ],
        "sugestoes_estrategicas": [
            "Diversifique sua carteira para reduzir risco",
            "Monitore regularmente o desempenho de cada posição"
        ]
    }

