"""
Agente Assessor de Investimentos Completo
Analisa profundamente a carteira, compras/vendas, dividendos, setores e performance
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

def analisar_carteira_completa(
    user_id: int,
    positions: List[Dict[str, Any]],
    trades: List[Dict[str, Any]],
    dividendos: List[Dict[str, Any]],
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
    Análise completa da carteira com agente assessor de investimentos.
    
    Args:
        user_id: ID do usuário
        positions: Lista de posições abertas
        trades: Lista de todas as operações (compras e vendas)
        dividendos: Lista de dividendos recebidos
        ... outros parâmetros de performance
    
    Returns:
        Dict com análise completa e pareceres por ação
    """
    try:
        # 1. Coletar dados adicionais (setores, exposição, etc)
        dados_complementares = _coletar_dados_complementares(positions)
        
        # 2. Analisar estrutura da carteira
        estrutura_carteira = _analisar_estrutura_carteira(
            positions, trades, dividendos, total_investido, total_valor
        )
        
        # 3. Analisar performance por ação
        performance_acoes = _analisar_performance_acoes(
            positions, trades, dividendos, pnl_carteira, pnl_realizado
        )
        
        # 4. Analisar setores
        analise_setores = _analisar_setores(positions, estrutura_carteira)
        
        # 5. Formatar dados para o prompt da IA
        dados_formatados = _formatar_dados_completos(
            positions, trades, dividendos, estrutura_carteira, 
            performance_acoes, analise_setores, dados_complementares,
            pnl_carteira, pnl_realizado, pnl_total,
            rentabilidade_carteira, rentabilidade_realizada, rentabilidade_total,
            total_investido, total_valor, custo_vendas, receita_vendas
        )
        
        # 6. Criar prompt detalhado
        prompt = _criar_prompt_assessor_completo(dados_formatados)
        
        # 7. Chamar IA para análise completa
        analise_ia = _chamar_ia_assessor(prompt)
        
        return {
            "status": "ok",
            "analise_completa": analise_ia,
            "dados_estrutura": estrutura_carteira,
            "performance_acoes": performance_acoes,
            "analise_setores": analise_setores,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na análise completa: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "erro",
            "erro": str(e),
            "mensagem": "Erro ao realizar análise completa. Verifique se há API de IA configurada.",
            "timestamp": datetime.now().isoformat()
        }

def _coletar_dados_complementares(positions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Coleta dados complementares sobre as ações (setores, etc)"""
    dados = {}
    
    try:
        from data.price_collector import coletar_precos
        
        for pos in positions:
            ticker = pos.get('ticker', '')
            if not ticker:
                continue
            
            try:
                # Tentar buscar informações adicionais via yfinance ou Brapi
                # Por enquanto, vamos usar um mapeamento básico de setores conhecidos
                setor = _identificar_setor(ticker)
                dados[ticker] = {
                    "setor": setor,
                    "subsector": _identificar_subsector(ticker)
                }
            except Exception as e:
                logger.warning(f"⚠️  Erro ao coletar dados complementares para {ticker}: {e}")
                dados[ticker] = {
                    "setor": "Não identificado",
                    "subsector": "Não identificado"
                }
    except Exception as e:
        logger.warning(f"⚠️  Erro ao coletar dados complementares: {e}")
    
    return dados

def _identificar_setor(ticker: str) -> str:
    """Identifica o setor da ação baseado no ticker"""
    # Mapeamento básico de setores conhecidos da B3
    setores = {
        # Bancos
        "ITUB": "Financeiro", "ITUB4": "Financeiro",
        "BBAS": "Financeiro", "BBAS3": "Financeiro",
        "BBDC": "Financeiro", "BBDC4": "Financeiro",
        "SANB": "Financeiro", "SANB11": "Financeiro",
        # Petróleo
        "PETR": "Petróleo e Gás", "PETR4": "Petróleo e Gás", "PETR3": "Petróleo e Gás",
        # Energia
        "CMIG": "Energia Elétrica", "CMIG4": "Energia Elétrica",
        "CSMG": "Energia Elétrica", "CSMG3": "Energia Elétrica",
        # Seguros
        "BBSE": "Seguros", "BBSE3": "Seguros",
        # Tecnologia
        "SYN": "Tecnologia", "SYN3": "Tecnologia",
    }
    
    # Remover sufixos .SA se houver
    ticker_clean = ticker.replace(".SA", "").upper()
    
    # Tentar match exato primeiro
    if ticker_clean in setores:
        return setores[ticker_clean]
    
    # Tentar match parcial (ex: ITUB4 -> ITUB)
    for key, setor in setores.items():
        if ticker_clean.startswith(key) or key in ticker_clean:
            return setor
    
    return "Não identificado"

def _identificar_subsector(ticker: str) -> str:
    """Identifica o subsector da ação"""
    subsectores = {
        "ITUB": "Bancos", "ITUB4": "Bancos",
        "BBAS": "Bancos", "BBAS3": "Bancos",
        "BBDC": "Bancos", "BBDC4": "Bancos",
        "SANB": "Bancos", "SANB11": "Bancos",
        "PETR": "Exploração e Refino", "PETR4": "Exploração e Refino",
        "CMIG": "Geração de Energia", "CMIG4": "Geração de Energia",
        "CSMG": "Geração de Energia", "CSMG3": "Geração de Energia",
        "BBSE": "Seguros", "BBSE3": "Seguros",
        "SYN": "Software", "SYN3": "Software",
    }
    
    ticker_clean = ticker.replace(".SA", "").upper()
    
    if ticker_clean in subsectores:
        return subsectores[ticker_clean]
    
    for key, subsector in subsectores.items():
        if ticker_clean.startswith(key) or key in ticker_clean:
            return subsector
    
    return "Não identificado"

def _analisar_estrutura_carteira(
    positions: List[Dict[str, Any]],
    trades: List[Dict[str, Any]],
    dividendos: List[Dict[str, Any]],
    total_investido: float,
    total_valor: float
) -> Dict[str, Any]:
    """Analisa a estrutura da carteira"""
    
    # Calcular exposição por ação
    exposicao_por_acao = {}
    for pos in positions:
        ticker = pos.get('ticker', '')
        valor_posicao = pos.get('valor_posicao', 0) or 0
        if total_valor > 0:
            exposicao_percentual = (valor_posicao / total_valor) * 100
        else:
            exposicao_percentual = 0
        
        exposicao_por_acao[ticker] = {
            "valor": valor_posicao,
            "percentual": exposicao_percentual,
            "quantidade": pos.get('quantidade', 0)
        }
    
    # Analisar histórico de compras/vendas
    compras_por_ticker = {}
    vendas_por_ticker = {}
    
    for trade in trades:
        ticker = trade.get('ticker', '')
        side = trade.get('side', '').upper()
        quantity = float(trade.get('quantity', 0))
        price = float(trade.get('price', 0))
        trade_date = trade.get('trade_date', '')
        
        if side == 'BUY':
            if ticker not in compras_por_ticker:
                compras_por_ticker[ticker] = {
                    "total_quantidade": 0,
                    "total_investido": 0,
                    "operacoes": []
                }
            compras_por_ticker[ticker]["total_quantidade"] += quantity
            compras_por_ticker[ticker]["total_investido"] += quantity * price
            compras_por_ticker[ticker]["operacoes"].append({
                "data": trade_date,
                "quantidade": quantity,
                "preco": price
            })
        elif side == 'SELL':
            if ticker not in vendas_por_ticker:
                vendas_por_ticker[ticker] = {
                    "total_quantidade": 0,
                    "total_receita": 0,
                    "operacoes": []
                }
            vendas_por_ticker[ticker]["total_quantidade"] += quantity
            vendas_por_ticker[ticker]["total_receita"] += quantity * price
            vendas_por_ticker[ticker]["operacoes"].append({
                "data": trade_date,
                "quantidade": quantity,
                "preco": price
            })
    
    # Analisar dividendos por ação
    dividendos_por_ticker = {}
    total_dividendos = 0
    
    for div in dividendos:
        ticker = div.get('ticker', '')
        valor_total = float(div.get('valor_total', 0))
        
        if ticker not in dividendos_por_ticker:
            dividendos_por_ticker[ticker] = {
                "total_recebido": 0,
                "quantidade_pagamentos": 0,
                "pagamentos": []
            }
        
        dividendos_por_ticker[ticker]["total_recebido"] += valor_total
        dividendos_por_ticker[ticker]["quantidade_pagamentos"] += 1
        dividendos_por_ticker[ticker]["pagamentos"].append({
            "data": div.get('data_pagamento', ''),
            "valor": valor_total,
            "tipo": div.get('tipo', 'DIVIDENDO')
        })
        total_dividendos += valor_total
    
    return {
        "exposicao_por_acao": exposicao_por_acao,
        "compras_por_ticker": compras_por_ticker,
        "vendas_por_ticker": vendas_por_ticker,
        "dividendos_por_ticker": dividendos_por_ticker,
        "total_dividendos": total_dividendos,
        "numero_acoes": len(positions),
        "concentracao": _calcular_concentracao(exposicao_por_acao)
    }

def _calcular_concentracao(exposicao_por_acao: Dict[str, Any]) -> Dict[str, Any]:
    """Calcula métricas de concentração da carteira"""
    if not exposicao_por_acao:
        return {"indice_herfindahl": 0, "maior_exposicao": 0, "concentrado": False}
    
    percentuais = [exp["percentual"] for exp in exposicao_por_acao.values()]
    
    # Índice de Herfindahl (soma dos quadrados das participações)
    indice_herfindahl = sum(p**2 for p in percentuais) / 10000  # Normalizado 0-1
    
    maior_exposicao = max(percentuais) if percentuais else 0
    
    # Considera concentrado se HHI > 0.25 (equivalente a 4 ações com 25% cada)
    concentrado = indice_herfindahl > 0.25 or maior_exposicao > 40
    
    return {
        "indice_herfindahl": indice_herfindahl,
        "maior_exposicao": maior_exposicao,
        "concentrado": concentrado,
        "diversificacao": "Baixa" if concentrado else "Adequada"
    }

def _analisar_performance_acoes(
    positions: List[Dict[str, Any]],
    trades: List[Dict[str, Any]],
    dividendos: List[Dict[str, Any]],
    pnl_carteira: float,
    pnl_realizado: float
) -> Dict[str, Any]:
    """Analisa performance detalhada de cada ação"""
    
    performance = {}
    
    for pos in positions:
        ticker = pos.get('ticker', '')
        quantidade = pos.get('quantidade', 0)
        preco_medio = pos.get('preco_medio', 0)
        preco_atual = pos.get('preco_ultimo')
        rentabilidade = pos.get('rentabilidade')
        valor_posicao = pos.get('valor_posicao', 0) or 0
        
        # Calcular dividendos recebidos para esta ação
        dividendos_acao = sum(
            float(d.get('valor_total', 0)) 
            for d in dividendos 
            if d.get('ticker') == ticker
        )
        
        # Calcular PnL não realizado
        pnl_nao_realizado = valor_posicao - (quantidade * preco_medio) if preco_atual else 0
        
        # Calcular PnL total (não realizado + dividendos)
        pnl_total_acao = pnl_nao_realizado + dividendos_acao
        
        # Rentabilidade total considerando dividendos
        investido_acao = quantidade * preco_medio
        rentabilidade_total = (pnl_total_acao / investido_acao) if investido_acao > 0 else 0
        
        performance[ticker] = {
            "quantidade": quantidade,
            "preco_medio": preco_medio,
            "preco_atual": preco_atual,
            "valor_posicao": valor_posicao,
            "investido": investido_acao,
            "pnl_nao_realizado": pnl_nao_realizado,
            "dividendos_recebidos": dividendos_acao,
            "pnl_total": pnl_total_acao,
            "rentabilidade": rentabilidade,
            "rentabilidade_total": rentabilidade_total,
            "contribuicao_pnl": pnl_total_acao  # Para ranking
        }
    
    # Ordenar por contribuição ao PnL
    ranking = sorted(
        performance.items(),
        key=lambda x: x[1].get('contribuicao_pnl', 0),
        reverse=True
    )
    
    return {
        "por_acao": performance,
        "ranking_melhores": [ticker for ticker, _ in ranking[:5] if ranking],
        "ranking_piores": [ticker for ticker, _ in reversed(ranking[-5:]) if ranking]
    }

def _analisar_setores(
    positions: List[Dict[str, Any]],
    estrutura_carteira: Dict[str, Any]
) -> Dict[str, Any]:
    """Analisa exposição por setores"""
    
    setores = {}
    dados_complementares = _coletar_dados_complementares(positions)
    
    for pos in positions:
        ticker = pos.get('ticker', '')
        valor_posicao = pos.get('valor_posicao', 0) or 0
        
        setor_info = dados_complementares.get(ticker, {})
        setor = setor_info.get('setor', 'Não identificado')
        subsector = setor_info.get('subsector', 'Não identificado')
        
        if setor not in setores:
            setores[setor] = {
                "valor_total": 0,
                "percentual": 0,
                "acoes": [],
                "subsectores": {}
            }
        
        setores[setor]["valor_total"] += valor_posicao
        setores[setor]["acoes"].append(ticker)
        
        if subsector not in setores[setor]["subsectores"]:
            setores[setor]["subsectores"][subsector] = {
                "valor_total": 0,
                "acoes": []
            }
        
        setores[setor]["subsectores"][subsector]["valor_total"] += valor_posicao
        setores[setor]["subsectores"][subsector]["acoes"].append(ticker)
    
    # Calcular percentuais
    total_valor = sum(s["valor_total"] for s in setores.values())
    for setor in setores.values():
        if total_valor > 0:
            setor["percentual"] = (setor["valor_total"] / total_valor) * 100
    
    return {
        "por_setor": setores,
        "total_setores": len(setores),
        "diversificacao_setorial": "Alta" if len(setores) >= 5 else "Média" if len(setores) >= 3 else "Baixa"
    }

def _formatar_dados_completos(
    positions: List[Dict[str, Any]],
    trades: List[Dict[str, Any]],
    dividendos: List[Dict[str, Any]],
    estrutura_carteira: Dict[str, Any],
    performance_acoes: Dict[str, Any],
    analise_setores: Dict[str, Any],
    dados_complementares: Dict[str, Any],
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
    """Formata todos os dados para o prompt da IA"""
    
    texto = f"""ANÁLISE COMPLETA DA CARTEIRA DE INVESTIMENTOS
Data da Análise: {datetime.now().strftime("%d/%m/%Y %H:%M")}

═══════════════════════════════════════════════════════════════
1. RESUMO EXECUTIVO
═══════════════════════════════════════════════════════════════

Total Investido (Posições Abertas): R$ {total_investido:,.2f}
Valor Atual (Posições Abertas): R$ {total_valor:,.2f}
PnL Carteira (Não Realizado): R$ {pnl_carteira:,.2f} ({rentabilidade_carteira*100:.2f}%)
PnL Realizado (Vendas): R$ {pnl_realizado:,.2f} ({rentabilidade_realizada*100:.2f}%)
PnL Total: R$ {pnl_total:,.2f} ({rentabilidade_total*100:.2f}%)
Total de Dividendos Recebidos: R$ {estrutura_carteira.get('total_dividendos', 0):,.2f}

═══════════════════════════════════════════════════════════════
2. ESTRUTURA DA CARTEIRA
═══════════════════════════════════════════════════════════════

Número de Ações na Carteira: {estrutura_carteira.get('numero_acoes', 0)}
Concentração: {"ALTA" if estrutura_carteira.get('concentracao', {}).get('concentrado') else "ADEQUADA"}
Índice de Herfindahl: {estrutura_carteira.get('concentracao', {}).get('indice_herfindahl', 0):.4f}
Maior Exposição Individual: {estrutura_carteira.get('concentracao', {}).get('maior_exposicao', 0):.2f}%

═══════════════════════════════════════════════════════════════
3. EXPOSIÇÃO POR AÇÃO
═══════════════════════════════════════════════════════════════
"""
    
    exposicao = estrutura_carteira.get('exposicao_por_acao', {})
    for ticker, exp in sorted(exposicao.items(), key=lambda x: x[1]['valor'], reverse=True):
        texto += f"\n{ticker}:"
        texto += f"\n  Valor: R$ {exp['valor']:,.2f} ({exp['percentual']:.2f}% da carteira)"
        texto += f"\n  Quantidade: {exp['quantidade']:.0f} ações"
    
    texto += f"\n\n═══════════════════════════════════════════════════════════════"
    texto += f"\n4. ANÁLISE POR SETORES"
    texto += f"\n═══════════════════════════════════════════════════════════════\n"
    
    setores = analise_setores.get('por_setor', {})
    for setor, dados in sorted(setores.items(), key=lambda x: x[1]['valor_total'], reverse=True):
        texto += f"\n{setor}:"
        texto += f"\n  Valor Total: R$ {dados['valor_total']:,.2f} ({dados['percentual']:.2f}%)"
        texto += f"\n  Ações: {', '.join(dados['acoes'])}"
        if dados.get('subsectores'):
            texto += f"\n  Subsectores:"
            for subsector, sub_dados in dados['subsectores'].items():
                texto += f"\n    - {subsector}: R$ {sub_dados['valor_total']:,.2f}"
    
    texto += f"\n\n═══════════════════════════════════════════════════════════════"
    texto += f"\n5. PERFORMANCE DETALHADA POR AÇÃO"
    texto += f"\n═══════════════════════════════════════════════════════════════\n"
    
    performance = performance_acoes.get('por_acao', {})
    for ticker, perf in sorted(performance.items(), key=lambda x: x[1].get('contribuicao_pnl', 0), reverse=True):
        texto += f"\n{ticker}:"
        texto += f"\n  Quantidade: {perf['quantidade']:.0f} ações"
        texto += f"\n  Preço Médio: R$ {perf['preco_medio']:.2f}"
        texto += f"\n  Preço Atual: R$ {perf['preco_atual']:.2f}" if perf['preco_atual'] else "\n  Preço Atual: Não disponível"
        texto += f"\n  Investido: R$ {perf['investido']:,.2f}"
        texto += f"\n  Valor Atual: R$ {perf['valor_posicao']:,.2f}"
        texto += f"\n  PnL Não Realizado: R$ {perf['pnl_nao_realizado']:,.2f}"
        texto += f"\n  Dividendos Recebidos: R$ {perf['dividendos_recebidos']:,.2f}"
        texto += f"\n  PnL Total: R$ {perf['pnl_total']:,.2f}"
        texto += f"\n  Rentabilidade: {perf['rentabilidade']*100:.2f}%" if perf['rentabilidade'] else "\n  Rentabilidade: N/A"
        texto += f"\n  Rentabilidade Total (com dividendos): {perf['rentabilidade_total']*100:.2f}%"
        
        # Adicionar histórico de compras/vendas
        compras = estrutura_carteira.get('compras_por_ticker', {}).get(ticker, {})
        if compras:
            texto += f"\n  Histórico de Compras:"
            texto += f"\n    Total: {compras.get('total_quantidade', 0):.0f} ações, R$ {compras.get('total_investido', 0):,.2f}"
            texto += f"\n    Operações: {len(compras.get('operacoes', []))}"
        
        vendas = estrutura_carteira.get('vendas_por_ticker', {}).get(ticker, {})
        if vendas:
            texto += f"\n  Histórico de Vendas:"
            texto += f"\n    Total: {vendas.get('total_quantidade', 0):.0f} ações, R$ {vendas.get('total_receita', 0):,.2f}"
            texto += f"\n    Operações: {len(vendas.get('operacoes', []))}"
        
        dividendos_ticker = estrutura_carteira.get('dividendos_por_ticker', {}).get(ticker, {})
        if dividendos_ticker:
            texto += f"\n  Dividendos:"
            texto += f"\n    Total Recebido: R$ {dividendos_ticker.get('total_recebido', 0):,.2f}"
            texto += f"\n    Pagamentos: {dividendos_ticker.get('quantidade_pagamentos', 0)}"
    
    texto += f"\n\n═══════════════════════════════════════════════════════════════"
    texto += f"\n6. RANKING DE PERFORMANCE"
    texto += f"\n═══════════════════════════════════════════════════════════════\n"
    
    ranking_melhores = performance_acoes.get('ranking_melhores', [])
    ranking_piores = performance_acoes.get('ranking_piores', [])
    
    texto += f"\nMelhores Performances:\n"
    for i, ticker in enumerate(ranking_melhores, 1):
        perf = performance.get(ticker, {})
        texto += f"  {i}. {ticker}: PnL R$ {perf.get('pnl_total', 0):,.2f} ({perf.get('rentabilidade_total', 0)*100:.2f}%)\n"
    
    texto += f"\nPiores Performances:\n"
    for i, ticker in enumerate(ranking_piores, 1):
        perf = performance.get(ticker, {})
        texto += f"  {i}. {ticker}: PnL R$ {perf.get('pnl_total', 0):,.2f} ({perf.get('rentabilidade_total', 0)*100:.2f}%)\n"
    
    return texto

def _criar_prompt_assessor_completo(dados_formatados: str) -> str:
    """Cria prompt completo para o assessor de investimentos"""
    
    return f"""Você é um assessor de investimentos sênior especializado em análise de carteiras de ações brasileiras (B3).

Sua função é realizar uma análise PROFUNDA e COMPLETA da carteira do cliente, emitindo pareceres detalhados para cada ação e recomendações estratégicas.

ANÁLISE SOLICITADA:

{dados_formatados}

INSTRUÇÕES PARA A ANÁLISE:

1. ANÁLISE INDIVIDUAL POR AÇÃO:
   Para CADA ação na carteira, forneça:
   - Parecer detalhado sobre a performance
   - Análise da rentabilidade (considerando dividendos)
   - Avaliação do timing de compras/vendas
   - Recomendação específica (MANTER, AUMENTAR, REDUZIR, VENDER)
   - Justificativa fundamentada
   - Perspectiva de curto/médio prazo

2. ANÁLISE DE SETORES:
   - Avaliar diversificação setorial
   - Identificar concentrações excessivas
   - Sugerir ajustes de alocação por setor
   - Considerar ciclos econômicos e tendências

3. ANÁLISE DE EXPOSIÇÃO:
   - Avaliar concentração da carteira
   - Identificar riscos de concentração excessiva
   - Sugerir diversificação se necessário
   - Avaliar tamanho das posições

4. ANÁLISE DE PERFORMANCE:
   - Comparar performance entre ações
   - Identificar ações que estão contribuindo positivamente
   - Identificar ações que estão prejudicando a carteira
   - Avaliar eficiência das operações (compras/vendas)

5. ANÁLISE DE DIVIDENDOS:
   - Avaliar yield de dividendos por ação
   - Considerar dividendos na rentabilidade total
   - Identificar ações com bom histórico de distribuição

6. RECOMENDAÇÕES ESTRATÉGICAS GERAIS:
   - Sugestões de rebalanceamento
   - Oportunidades de otimização
   - Alertas sobre riscos identificados
   - Estratégias de longo prazo

FORMATO DE RESPOSTA (JSON):

{{
  "resumo_executivo": "Resumo executivo da análise em 3-4 parágrafos",
  "pareceres_por_acao": [
    {{
      "ticker": "PETR4",
      "parecer": "Análise detalhada e fundamentada da ação...",
      "recomendacao": "MANTER|AUMENTAR|REDUZIR|VENDER",
      "justificativa": "Justificativa detalhada da recomendação...",
      "prioridade": "ALTA|MEDIA|BAIXA",
      "rentabilidade_atual": "X%",
      "rentabilidade_com_dividendos": "X%",
      "avaliacao_timing": "Avaliação do timing de compras/vendas...",
      "perspectiva_curto_prazo": "Perspectiva para próximos 3-6 meses...",
      "perspectiva_medio_prazo": "Perspectiva para próximos 6-12 meses...",
      "yield_dividendos": "X%",
      "pontos_fortes": ["Ponto forte 1", "Ponto forte 2"],
      "pontos_fracos": ["Ponto fraco 1", "Ponto fraco 2"],
      "acao_sugerida": "Descrição específica da ação recomendada (ex: 'Reduzir 30% da posição')"
    }}
  ],
  "analise_setores": {{
    "diversificacao": "Avaliação da diversificação setorial...",
    "setores_sobrepeso": ["Setor 1", "Setor 2"],
    "setores_subpeso": ["Setor 1", "Setor 2"],
    "recomendacoes_setoriais": [
      "Recomendação 1 sobre setores",
      "Recomendação 2 sobre setores"
    ]
  }},
  "analise_exposicao": {{
    "concentracao": "Avaliação da concentração da carteira...",
    "riscos_identificados": ["Risco 1", "Risco 2"],
    "recomendacoes_diversificacao": [
      "Recomendação 1 sobre diversificação",
      "Recomendação 2 sobre diversificação"
    ]
  }},
  "analise_performance": {{
    "acoes_destaque_positivo": ["Ticker1", "Ticker2"],
    "acoes_destaque_negativo": ["Ticker1", "Ticker2"],
    "eficiencia_operacoes": "Avaliação da eficiência das operações...",
    "sugestoes_otimizacao": [
      "Sugestão 1",
      "Sugestão 2"
    ]
  }},
  "recomendacoes_estrategicas": [
    "Recomendação estratégica 1",
    "Recomendação estratégica 2",
    "Recomendação estratégica 3"
  ],
  "alertas": [
    "Alerta 1 se houver",
    "Alerta 2 se houver"
  ],
  "proximos_passos": [
    "Próximo passo 1",
    "Próximo passo 2"
  ]
}}

IMPORTANTE:
- Seja detalhado e fundamentado em cada parecer
- Considere TODOS os aspectos: performance, dividendos, setores, exposição
- Forneça recomendações práticas e acionáveis
- Seja honesto sobre riscos e pontos fracos
- Responda APENAS com JSON válido, sem texto adicional antes ou depois.
"""

def _chamar_ia_assessor(prompt: str) -> Dict[str, Any]:
    """Chama a API de IA para análise completa do assessor"""
    # Reutilizar a mesma lógica de chamada de IA (já tem retry e tratamento de erros)
    from core.ia_advisor import _chamar_ia
    return _chamar_ia(prompt)

