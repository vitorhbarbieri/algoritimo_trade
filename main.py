"""
Main: Pipeline completo do sistema de trading algorítmico
1) Coleta dados
2) Gera features
3) Roda estratégias
4) Combina sinais
5) Aplica risk manager
6) Simula execução
7) Logs
"""
import sys
import os

# Adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.price_collector import coletar_precos
from data.news_collector import coletar_noticias_brasileiras
from data.preprocess import preparar_dados_completos
from features.technical_indicators import calcular_todos_indicadores
from features.statistical_features import calcular_todas_features_estatisticas
from features.sentiment_engine import analisar_sentimento_noticias
from strategies.trend_strategy import gerar_sinal_tendencia
from strategies.mean_reversion_strategy import gerar_sinal_reversao
from strategies.news_strategy import gerar_sinal_noticias
from core.signal_orchestrator import SignalOrchestrator
from core.risk_manager import RiskManager
from core.trade_executor import TradeExecutor
from utils.config import (
    TICKERS, PERIODO_PADRAO, PESOS_ESTRATEGIAS,
    RISCO_POR_TRADE, CAPITAL_INICIAL
)
from utils.logger import (
    log_info, log_error, log_warning, log_trade, log_sinal
)


def pipeline_completo(ticker: str = None, modo_backtest: bool = False):
    """
    Executa pipeline completo do sistema
    
    Args:
        ticker: Código do ativo (se None, usa primeiro de TICKERS)
        modo_backtest: Se True, executa backtest ao invés de simulação
    """
    if ticker is None:
        ticker = TICKERS[0]
    
    log_info("="*70)
    log_info(f"🚀 INICIANDO PIPELINE - {ticker}")
    log_info("="*70)
    
    # 1) COLETA DE DADOS
    log_info("\n[1/7] Coletando dados de preços...")
    try:
        df_precos = coletar_precos(ticker, periodo=PERIODO_PADRAO, intervalo='1d')
        log_info(f"✅ Dados coletados: {len(df_precos)} períodos")
    except Exception as e:
        log_error(f"❌ Erro ao coletar preços: {e}")
        return
    
    log_info("\n[2/7] Coletando notícias...")
    try:
        noticias = coletar_noticias_brasileiras()
        log_info(f"✅ Notícias coletadas: {len(noticias)}")
    except Exception as e:
        log_warning(f"⚠️  Erro ao coletar notícias: {e}")
        noticias = []
    
    # 2) PREPROCESSAMENTO
    log_info("\n[3/7] Preprocessando dados...")
    try:
        df = preparar_dados_completos(df_precos, noticias, janela_horaria='1D')
        log_info(f"✅ Dados preparados: {df.shape}")
    except Exception as e:
        log_error(f"❌ Erro no preprocessamento: {e}")
        df = df_precos
    
    # 3) FEATURES
    log_info("\n[4/7] Calculando indicadores técnicos...")
    try:
        df = calcular_todos_indicadores(df)
        log_info("✅ Indicadores técnicos calculados")
    except Exception as e:
        log_error(f"❌ Erro ao calcular indicadores: {e}")
    
    log_info("Calculando features estatísticas...")
    try:
        df = calcular_todas_features_estatisticas(df)
        log_info("✅ Features estatísticas calculadas")
    except Exception as e:
        log_warning(f"⚠️  Erro ao calcular features estatísticas: {e}")
    
    # 4) ESTRATÉGIAS
    log_info("\n[5/7] Gerando sinais das estratégias...")
    
    sinal_trend = None
    sinal_reversao = None
    sinal_news = None
    
    try:
        sinal_trend = gerar_sinal_tendencia(df)
        log_info(f"✅ Estratégia de tendência: {len(sinal_trend[sinal_trend != 0])} sinais")
    except Exception as e:
        log_warning(f"⚠️  Erro na estratégia de tendência: {e}")
    
    try:
        sinal_reversao = gerar_sinal_reversao(df)
        log_info(f"✅ Estratégia de reversão: {len(sinal_reversao[sinal_reversao != 0])} sinais")
    except Exception as e:
        log_warning(f"⚠️  Erro na estratégia de reversão: {e}")
    
    try:
        import pandas as pd
        sentimento = analisar_sentimento_noticias(noticias)
        sinal_news_valor = gerar_sinal_noticias(noticias)
        # Criar Series com mesmo índice do DataFrame
        sinal_news = pd.Series([sinal_news_valor] * len(df), index=df.index)
        log_info(f"✅ Estratégia de notícias: Sentimento = {sentimento:+.3f}, Sinal = {sinal_news_valor}")
    except Exception as e:
        log_warning(f"⚠️  Erro na estratégia de notícias: {e}")
        import pandas as pd
        sinal_news = pd.Series(0, index=df.index)
    
    # 5) ORQUESTRAÇÃO
    log_info("\n[6/7] Combinando sinais...")
    try:
        orchestrator = SignalOrchestrator(pesos=PESOS_ESTRATEGIAS)
        sinal_final = orchestrator.combinar_sinais(sinal_trend, sinal_reversao, sinal_news)
        confianca = orchestrator.calcular_confianca(sinal_trend, sinal_reversao, sinal_news)
        
        log_info(f"✅ Sinal final gerado: {len(sinal_final[sinal_final != 0])} sinais não-neutros")
        
        # Mostrar últimos sinais
        ultimos_sinais = sinal_final.tail(5)
        for idx, sinal in ultimos_sinais.items():
            if sinal != 0:
                conf = confianca.get(idx, 0.5) if isinstance(confianca, pd.Series) else 0.5
                log_sinal(ticker, int(sinal), conf)
    except Exception as e:
        log_error(f"❌ Erro na orquestração: {e}")
        return
    
    # 6) RISK MANAGER E EXECUÇÃO
    log_info("\n[7/7] Aplicando gestão de risco e executando trades...")
    
    risk_manager = RiskManager(risco_por_trade=RISCO_POR_TRADE)
    executor = TradeExecutor(modo_mock=True)
    
    capital = CAPITAL_INICIAL
    posicao_aberta = False
    
    # Simular execução nos últimos 5 dias
    ultimos_dias = df.tail(5)
    
    for idx, row in ultimos_dias.iterrows():
        sinal = sinal_final.get(idx, 0)
        
        if sinal != 0 and not posicao_aberta:
            preco = row['Close']
            atr = row.get('ATR', preco * 0.02)
            
            stop_loss = risk_manager.calcular_stop_loss(preco, int(sinal), atr)
            take_profit = risk_manager.calcular_take_profit(preco, int(sinal), atr)
            quantidade = risk_manager.calcular_tamanho_posicao(capital, preco, stop_loss, int(sinal))
            
            if quantidade > 0:
                operacao = executor.executar_compra(ticker, quantidade, preco, idx)
                capital -= operacao['valor_total']
                posicao_aberta = True
                log_info(f"💰 Capital restante: R$ {capital:.2f}")
    
    # Resumo final
    log_info("\n" + "="*70)
    log_info("📊 RESUMO FINAL")
    log_info("="*70)
    log_info(f"Ticker: {ticker}")
    log_info(f"Períodos analisados: {len(df)}")
    log_info(f"Sinais gerados: {len(sinal_final[sinal_final != 0])}")
    log_info(f"Capital inicial: R$ {CAPITAL_INICIAL:.2f}")
    log_info(f"Capital final: R$ {capital:.2f}")
    log_info(f"Retorno: {((capital - CAPITAL_INICIAL) / CAPITAL_INICIAL * 100):+.2f}%")
    log_info("="*70)


if __name__ == "__main__":
    import pandas as pd
    
    # Executar pipeline
    ticker = sys.argv[1] if len(sys.argv) > 1 else None
    pipeline_completo(ticker)

