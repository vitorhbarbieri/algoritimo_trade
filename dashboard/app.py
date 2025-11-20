"""
Dashboard web para controle e visualização do sistema de trading
"""
from flask import Flask, render_template, jsonify, request
import sys
import os
from datetime import datetime
import pandas as pd
import traceback

# Adicionar diretórios ao path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

try:
    from data.price_collector import coletar_precos
    from data.news_collector import coletar_noticias_brasileiras
    from features.technical_indicators import calcular_todos_indicadores
    from features.statistical_features import calcular_todas_features_estatisticas
    from features.sentiment_engine import analisar_sentimento_noticias
    from strategies.trend_strategy import gerar_sinal_tendencia
    from strategies.mean_reversion_strategy import gerar_sinal_reversao
    from strategies.news_strategy import gerar_sinal_noticias
    from core.signal_orchestrator import SignalOrchestrator
    from core.trade_executor import TradeExecutor
    from utils.config import TICKERS, PESOS_ESTRATEGIAS, CAPITAL_INICIAL
    from utils.logger import log_info
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print(f"Base dir: {base_dir}")
    traceback.print_exc()
    # Valores padrão caso falhe
    TICKERS = ['ITUB4.SA']
    PESOS_ESTRATEGIAS = {'trend': 0.4, 'reversao': 0.3, 'news': 0.3}
    CAPITAL_INICIAL = 10000.0

app = Flask(__name__)

# Estado global do sistema
try:
    executor = TradeExecutor(modo_mock=True)
except:
    executor = None
    print("⚠️  Aviso: TradeExecutor não pôde ser inicializado")

capital_atual = CAPITAL_INICIAL if 'CAPITAL_INICIAL' in globals() else 10000.0


@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Retorna status atual do sistema"""
    try:
        if executor is None:
            return jsonify({
                'capital_atual': capital_atual,
                'capital_inicial': CAPITAL_INICIAL if 'CAPITAL_INICIAL' in globals() else 10000.0,
                'retorno_percentual': 0.0,
                'posicoes_abertas': 0,
                'total_operacoes': 0,
                'timestamp': datetime.now().isoformat(),
                'erro': 'Executor não inicializado'
            })
        
        posicoes = executor.obter_posicoes_abertas()
        historico = executor.obter_historico()
        
        capital_inicial = CAPITAL_INICIAL if 'CAPITAL_INICIAL' in globals() else 10000.0
        
        return jsonify({
            'capital_atual': capital_atual,
            'capital_inicial': capital_inicial,
            'retorno_percentual': ((capital_atual - capital_inicial) / capital_inicial * 100) if capital_inicial > 0 else 0,
            'posicoes_abertas': len(posicoes) if posicoes else 0,
            'total_operacoes': len(historico) if not historico.empty else 0,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'erro': str(e),
            'capital_atual': capital_atual,
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/analisar/<ticker>')
def analisar_ticker(ticker):
    """Analisa um ticker e retorna sinais"""
    try:
        # Coletar dados
        df_precos = coletar_precos(ticker, periodo='1mo', intervalo='1d')
        if df_precos.empty:
            return jsonify({'erro': 'Nenhum dado encontrado para o ticker'}), 404
        
        noticias = []
        try:
            noticias = coletar_noticias_brasileiras()
        except Exception as e:
            print(f"Erro ao coletar notícias: {e}")
        
        # Calcular features
        df = calcular_todos_indicadores(df_precos)
        try:
            df = calcular_todas_features_estatisticas(df)
        except Exception as e:
            print(f"Erro ao calcular features estatísticas: {e}")
        
        # Gerar sinais
        sinal_trend = pd.Series(0, index=df.index)
        sinal_reversao = pd.Series(0, index=df.index)
        sinal_news_valor = 0
        sentimento = 0.0
        
        try:
            sinal_trend = gerar_sinal_tendencia(df)
        except Exception as e:
            print(f"Erro na estratégia de tendência: {e}")
        
        try:
            sinal_reversao = gerar_sinal_reversao(df)
        except Exception as e:
            print(f"Erro na estratégia de reversão: {e}")
        
        try:
            sentimento = analisar_sentimento_noticias(noticias)
            sinal_news_valor = gerar_sinal_noticias(noticias)
        except Exception as e:
            print(f"Erro na estratégia de notícias: {e}")
        
        sinal_news = pd.Series([sinal_news_valor] * len(df), index=df.index)
        
        # Combinar sinais
        try:
            orchestrator = SignalOrchestrator(pesos=PESOS_ESTRATEGIAS)
            sinal_final = orchestrator.combinar_sinais(sinal_trend, sinal_reversao, sinal_news)
            confianca = orchestrator.calcular_confianca(sinal_trend, sinal_reversao, sinal_news)
        except Exception as e:
            print(f"Erro na orquestração: {e}")
            sinal_final = pd.Series(0, index=df.index)
            confianca = pd.Series(0.5, index=df.index)
        
        # Último sinal
        ultimo_sinal = sinal_final.iloc[-1] if len(sinal_final) > 0 else 0
        ultima_confianca = confianca.iloc[-1] if len(confianca) > 0 else 0.5
        
        # Dados do preço
        ultimo_preco = df['Close'].iloc[-1]
        rsi = df['RSI'].iloc[-1] if 'RSI' in df.columns and pd.notna(df['RSI'].iloc[-1]) else None
        macd = df['MACD'].iloc[-1] if 'MACD' in df.columns and pd.notna(df['MACD'].iloc[-1]) else None
        
        return jsonify({
            'ticker': ticker,
            'preco_atual': float(ultimo_preco),
            'sinal_final': int(ultimo_sinal),
            'confianca': float(ultima_confianca),
            'sentimento_noticias': float(sentimento),
            'rsi': float(rsi) if rsi is not None else None,
            'macd': float(macd) if macd is not None else None,
            'sinal_trend': int(sinal_trend.iloc[-1]) if len(sinal_trend) > 0 else 0,
            'sinal_reversao': int(sinal_reversao.iloc[-1]) if len(sinal_reversao) > 0 else 0,
            'sinal_news': int(sinal_news_valor),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Erro completo: {error_msg}")
        return jsonify({'erro': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/api/operacoes')
def get_operacoes():
    """Retorna histórico de operações"""
    try:
        if executor is None:
            return jsonify({'operacoes': []})
        
        historico = executor.obter_historico()
        
        if historico.empty:
            return jsonify({'operacoes': []})
        
        operacoes = historico.to_dict('records')
        for op in operacoes:
            if 'timestamp' in op and pd.notna(op['timestamp']):
                op['timestamp'] = op['timestamp'].isoformat() if hasattr(op['timestamp'], 'isoformat') else str(op['timestamp'])
        
        return jsonify({'operacoes': operacoes})
    except Exception as e:
        return jsonify({'operacoes': [], 'erro': str(e)})


@app.route('/api/posicoes')
def get_posicoes():
    """Retorna posições abertas"""
    try:
        if executor is None:
            return jsonify({'posicoes': {}})
        
        posicoes = executor.obter_posicoes_abertas()
        
        return jsonify({'posicoes': posicoes})
    except Exception as e:
        return jsonify({'posicoes': {}, 'erro': str(e)})


@app.route('/api/tickers')
def get_tickers():
    """Retorna lista de tickers disponíveis"""
    try:
        # Lista atualizada com todos os ativos
        tickers_lista = [
            'BBSE3.SA',  # Banco do Brasil
            'CMIG4.SA',  # Cemig
            'CSMG3.SA',  # Copasa
            'ITUB4.SA',  # Itaú
            'PETR4.SA',  # Petrobras
            'SANB11.SA', # Santander
            'SYN3.SA'    # SYN
        ]
        
        # Tentar usar TICKERS do config, senão usar lista padrão
        if 'TICKERS' in globals() and TICKERS:
            tickers = TICKERS
        else:
            tickers = tickers_lista
        
        return jsonify({'tickers': tickers})
    except Exception as e:
        # Em caso de erro, retornar lista padrão
        return jsonify({
            'tickers': [
                'BBSE3.SA',
                'CMIG4.SA',
                'CSMG3.SA',
                'ITUB4.SA',
                'PETR4.SA',
                'SANB11.SA',
                'SYN3.SA'
            ],
            'erro': str(e)
        })


if __name__ == '__main__':
    # Para produção, usar variável de ambiente PORT
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    try:
        print("="*70)
        print("🚀 Iniciando Dashboard Algoritimo Trade")
        print("="*70)
        print(f"📊 Acesse: http://localhost:{port}")
        print(f"📊 Ou: http://127.0.0.1:{port}")
        print("="*70)
        print("\nPressione Ctrl+C para parar o servidor\n")
        
        if 'log_info' in globals():
            log_info("🚀 Iniciando dashboard...")
            log_info(f"📊 Acesse: http://localhost:{port}")
        
        app.run(debug=debug_mode, host='0.0.0.0', port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n⚠️  Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        traceback.print_exc()

