"""
Script de teste para verificar se o dashboard pode ser iniciado
"""
import sys
import os

# Adicionar diretórios ao path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

print("="*70)
print("🔍 TESTE DE IMPORTAÇÕES DO DASHBOARD")
print("="*70)

try:
    print("\n[1/10] Importando Flask...")
    from flask import Flask
    print("✅ Flask importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar Flask: {e}")
    sys.exit(1)

try:
    print("\n[2/10] Importando módulos de data...")
    from data.price_collector import coletar_precos
    from data.news_collector import coletar_noticias_brasileiras
    print("✅ Módulos de data importados")
except Exception as e:
    print(f"❌ Erro ao importar módulos de data: {e}")

try:
    print("\n[3/10] Importando módulos de features...")
    from features.technical_indicators import calcular_todos_indicadores
    from features.statistical_features import calcular_todas_features_estatisticas
    from features.sentiment_engine import analisar_sentimento_noticias
    print("✅ Módulos de features importados")
except Exception as e:
    print(f"❌ Erro ao importar módulos de features: {e}")

try:
    print("\n[4/10] Importando estratégias...")
    from strategies.trend_strategy import gerar_sinal_tendencia
    from strategies.mean_reversion_strategy import gerar_sinal_reversao
    from strategies.news_strategy import gerar_sinal_noticias
    print("✅ Estratégias importadas")
except Exception as e:
    print(f"❌ Erro ao importar estratégias: {e}")

try:
    print("\n[5/10] Importando core...")
    from core.signal_orchestrator import SignalOrchestrator
    from core.trade_executor import TradeExecutor
    print("✅ Core importado")
except Exception as e:
    print(f"❌ Erro ao importar core: {e}")

try:
    print("\n[6/10] Importando utils...")
    from utils.config import TICKERS, PESOS_ESTRATEGIAS, CAPITAL_INICIAL
    from utils.logger import log_info
    print("✅ Utils importados")
except Exception as e:
    print(f"❌ Erro ao importar utils: {e}")

print("\n" + "="*70)
print("✅ TESTE CONCLUÍDO")
print("="*70)
print("\nSe todos os módulos foram importados com sucesso,")
print("o dashboard deve funcionar. Execute: python app.py")










