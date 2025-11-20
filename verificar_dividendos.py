#!/usr/bin/env python
"""Script para verificar dividendos no banco de dados"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.trades_repository import list_dividendos, calculate_total_dividendos, init_db

# Inicializar banco
init_db()

# Listar dividendos
divs = list_dividendos()
print(f"\n📊 Total de dividendos cadastrados: {len(divs)}")

if divs:
    print("\n📋 Primeiros 5 dividendos:")
    for d in divs[:5]:
        print(f"  - {d['ticker']}: R$ {d['valor_total']:.2f} em {d['data_pagamento']} ({d['tipo']})")
else:
    print("\n⚠️  Nenhum dividendo encontrado no banco de dados!")
    print("   Você precisa importar dividendos primeiro.")

# Calcular totais
totals = calculate_total_dividendos()
print(f"\n💰 Total geral de dividendos: R$ {totals['total_geral']:.2f}")

if totals['por_ticker']:
    print("\n📈 Dividendos por ticker:")
    for ticker, valor in totals['por_ticker'].items():
        print(f"  - {ticker}: R$ {valor:.2f}")
else:
    print("\n⚠️  Nenhum dividendo por ticker encontrado.")

