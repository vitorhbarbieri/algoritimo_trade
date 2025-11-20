#!/usr/bin/env python
"""Testa a função corrigida de coleta de dividendos"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.dividendos_collector import coletar_dividendos_brapi

print("🧪 Testando função coletar_dividendos_brapi...\n")

tickers_teste = ["PETR4", "ITUB4", "VALE3"]

for ticker in tickers_teste:
    print(f"\n{'='*70}")
    print(f"📊 Testando {ticker}")
    print('='*70)
    
    try:
        dividendos = coletar_dividendos_brapi(ticker, limit=10)
        
        print(f"\n✅ Total encontrado: {len(dividendos)} dividendos")
        
        if dividendos:
            print("\n📋 Primeiros 5 dividendos:")
            for i, div in enumerate(dividendos[:5], 1):
                print(f"  {i}. {div['data_pagamento']}: R$ {div['valor_por_acao']:.4f} por ação ({div['tipo']})")
        else:
            print("⚠️  Nenhum dividendo encontrado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
print("✅ Teste concluído!")

