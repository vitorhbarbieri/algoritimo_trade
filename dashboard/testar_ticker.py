"""
Script para testar se um ticker específico funciona
"""
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from data.price_collector import coletar_precos

print("="*70)
print("🧪 TESTE DE TICKERS")
print("="*70)

tickers_teste = [
    'BBSE3.SA',
    'CMIG4.SA',
    'CSMG3.SA',
    'ITUB4.SA',
    'PETR4.SA',
    'SANB11.SA',
    'SYN3.SA'
]

for ticker in tickers_teste:
    print(f"\n{'='*70}")
    print(f"Testando: {ticker}")
    print(f"{'='*70}")
    
    try:
        df = coletar_precos(ticker, periodo='1mo', intervalo='1d')
        print(f"✅ SUCESSO!")
        print(f"   Períodos: {len(df)}")
        print(f"   Primeiro preço: R$ {df['Close'].iloc[0]:.2f}")
        print(f"   Último preço: R$ {df['Close'].iloc[-1]:.2f}")
        print(f"   Variação: {((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100):+.2f}%")
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print(f"   Este ticker pode estar incorreto ou não ter dados disponíveis")

print(f"\n{'='*70}")
print("✅ TESTE CONCLUÍDO")
print(f"{'='*70}")






