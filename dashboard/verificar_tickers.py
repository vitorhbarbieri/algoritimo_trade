"""
Script para verificar se os tickers estão corretos
"""
import json

# Tickers esperados
TICKERS_ESPERADOS = [
    'BBSE3.SA',
    'CMIG4.SA',
    'CSMG3.SA',
    'ITUB4.SA',
    'PETR4.SA',
    'SANB11.SA',
    'SYN3.SA'
]

print("="*70)
print("🔍 VERIFICAÇÃO DE TICKERS")
print("="*70)

# Verificar app_simples.py
print("\n[1/3] Verificando app_simples.py...")
try:
    with open('app_simples.py', 'r', encoding='utf-8') as f:
        conteudo = f.read()
        if 'BBSE3.SA' in conteudo:
            print("✅ BBSE3.SA encontrado")
        else:
            print("❌ BBSE3.SA NÃO encontrado")
        
        if 'BB5E3.SA' in conteudo:
            print("⚠️  BB5E3.SA ainda presente (deve ser BBSE3.SA)")
        
        # Contar quantos tickers estão na lista
        tickers_encontrados = []
        for ticker in TICKERS_ESPERADOS:
            if ticker in conteudo:
                tickers_encontrados.append(ticker)
        
        print(f"\n✅ Tickers corretos encontrados: {len(tickers_encontrados)}/7")
        for ticker in tickers_encontrados:
            print(f"   ✅ {ticker}")
        
        faltando = [t for t in TICKERS_ESPERADOS if t not in tickers_encontrados]
        if faltando:
            print(f"\n❌ Tickers faltando:")
            for ticker in faltando:
                print(f"   ❌ {ticker}")
except Exception as e:
    print(f"❌ Erro ao verificar: {e}")

# Verificar config.py
print("\n[2/3] Verificando utils/config.py...")
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.config import TICKERS
    
    print(f"✅ Tickers no config: {len(TICKERS)}")
    for ticker in TICKERS:
        if ticker in TICKERS_ESPERADOS:
            print(f"   ✅ {ticker}")
        else:
            print(f"   ⚠️  {ticker} (não está na lista esperada)")
    
    faltando = [t for t in TICKERS_ESPERADOS if t not in TICKERS]
    if faltando:
        print(f"\n❌ Tickers faltando no config:")
        for ticker in faltando:
            print(f"   ❌ {ticker}")
    
except Exception as e:
    print(f"❌ Erro ao verificar config: {e}")

print("\n[3/3] Lista esperada:")
for i, ticker in enumerate(TICKERS_ESPERADOS, 1):
    print(f"   {i}. {ticker}")

print("\n" + "="*70)
print("✅ VERIFICAÇÃO CONCLUÍDA")
print("="*70)










