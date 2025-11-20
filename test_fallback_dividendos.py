#!/usr/bin/env python
"""
Script para testar o sistema de fallback de dividendos
Testa todas as APIs disponíveis e mostra qual foi usada
"""
import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.dividendos_collector import coletar_dividendos, coletar_dividendos_brapi, coletar_dividendos_yfinance, coletar_dividendos_ibovfinancials
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def testar_todas_apis(ticker="PETR4"):
    """Testa todas as APIs individualmente"""
    print(f"\n{'='*70}")
    print(f"🧪 TESTE COMPLETO DE APIs - {ticker}")
    print(f"{'='*70}\n")
    
    resultados = {}
    
    # Teste 1: Brapi.dev
    print("1️⃣  Testando Brapi.dev...")
    try:
        dividendos = coletar_dividendos_brapi(ticker, limit=5)
        resultados['Brapi.dev'] = {
            'sucesso': len(dividendos) > 0,
            'quantidade': len(dividendos),
            'dados': dividendos[:2] if dividendos else []
        }
        print(f"   ✅ {len(dividendos)} dividendos encontrados\n")
    except Exception as e:
        resultados['Brapi.dev'] = {'sucesso': False, 'erro': str(e)[:100]}
        print(f"   ❌ Erro: {str(e)[:100]}\n")
    
    # Teste 2: IbovFinancials
    print("2️⃣  Testando IbovFinancials...")
    try:
        dividendos = coletar_dividendos_ibovfinancials(ticker, limit=5)
        resultados['IbovFinancials'] = {
            'sucesso': len(dividendos) > 0,
            'quantidade': len(dividendos),
            'dados': dividendos[:2] if dividendos else []
        }
        print(f"   ✅ {len(dividendos)} dividendos encontrados\n")
    except Exception as e:
        resultados['IbovFinancials'] = {'sucesso': False, 'erro': str(e)[:100]}
        print(f"   ❌ Erro: {str(e)[:100]}\n")
    
    # Teste 3: yfinance
    print("3️⃣  Testando yfinance...")
    try:
        dividendos = coletar_dividendos_yfinance(ticker, limit=5)
        resultados['yfinance'] = {
            'sucesso': len(dividendos) > 0,
            'quantidade': len(dividendos),
            'dados': dividendos[:2] if dividendos else []
        }
        print(f"   ✅ {len(dividendos)} dividendos encontrados\n")
    except Exception as e:
        resultados['yfinance'] = {'sucesso': False, 'erro': str(e)[:100]}
        print(f"   ❌ Erro: {str(e)[:100]}\n")
    
    return resultados

def testar_fallback_automatico(ticker="PETR4"):
    """Testa o sistema de fallback automático"""
    print(f"\n{'='*70}")
    print(f"🔄 TESTE DE FALLBACK AUTOMÁTICO - {ticker}")
    print(f"{'='*70}\n")
    
    try:
        dividendos, fonte = coletar_dividendos(ticker, limit=5)
        
        print(f"✅ Sucesso!")
        print(f"   📊 Fonte utilizada: {fonte}")
        print(f"   📈 Dividendos encontrados: {len(dividendos)}")
        
        if dividendos:
            print(f"\n📋 Primeiros dividendos:")
            for i, div in enumerate(dividendos[:3], 1):
                print(f"   {i}. Data Pagamento: {div['data_pagamento']}")
                print(f"      Data Ex-Dividendo: {div.get('data_ex_dividendo', 'N/A')}")
                print(f"      Valor: R$ {div['valor_por_acao']:.4f}")
                print(f"      Tipo: {div['tipo']}")
                print()
        
        return True, fonte, dividendos
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False, None, []

def testar_tickers_problematicos():
    """Testa com tickers que costumam dar problema no Brapi"""
    print(f"\n{'='*70}")
    print(f"🔍 TESTE COM TICKERS PROBLEMÁTICOS")
    print(f"{'='*70}\n")
    
    tickers = ["BBSE3", "PETR4", "ITUB4", "VALE3"]
    
    for ticker in tickers:
        print(f"\n📊 Testando {ticker}...")
        try:
            dividendos, fonte = coletar_dividendos(ticker, limit=3)
            status = "✅" if dividendos else "⚠️"
            print(f"   {status} Fonte: {fonte} | Dividendos: {len(dividendos)}")
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:80]}")

if __name__ == "__main__":
    print("🧪 TESTE DO SISTEMA DE FALLBACK DE DIVIDENDOS")
    print("=" * 70)
    
    # Teste 1: Testar todas as APIs individualmente
    resultados = testar_todas_apis("PETR4")
    
    # Teste 2: Testar fallback automático
    sucesso, fonte, dividendos = testar_fallback_automatico("PETR4")
    
    # Teste 3: Testar com tickers problemáticos
    testar_tickers_problematicos()
    
    # Resumo
    print(f"\n{'='*70}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*70}\n")
    
    print("APIs individuais:")
    for api, resultado in resultados.items():
        if resultado.get('sucesso'):
            print(f"  ✅ {api}: {resultado['quantidade']} dividendos")
        else:
            print(f"  ❌ {api}: {resultado.get('erro', 'Falhou')}")
    
    print(f"\nFallback automático:")
    if sucesso:
        print(f"  ✅ Funcionou! Fonte utilizada: {fonte}")
        print(f"  📈 {len(dividendos)} dividendos obtidos")
    else:
        print(f"  ❌ Falhou")
    
    print(f"\n{'='*70}")
    print("✅ TESTES CONCLUÍDOS")
    print(f"{'='*70}")


