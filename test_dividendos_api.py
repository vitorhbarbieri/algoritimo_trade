#!/usr/bin/env python
"""Script para testar a API de dividendos da Brapi.dev"""
import requests
import json
from datetime import datetime

def testar_api_dividendos(ticker="PETR4"):
    """Testa a API de dividendos da Brapi.dev"""
    print(f"\n🔍 Testando API de dividendos para {ticker}...")
    print("=" * 70)
    
    # Teste 1: Com parâmetro dividends=true
    url1 = f"https://brapi.dev/api/quote/{ticker}?dividends=true"
    print(f"\n📡 Teste 1: GET {url1}")
    try:
        resp1 = requests.get(url1, timeout=15)
        print(f"Status: {resp1.status_code}")
        
        if resp1.status_code == 200:
            data1 = resp1.json()
            print(f"Keys no JSON: {list(data1.keys())}")
            
            results = data1.get("results", [])
            print(f"Results count: {len(results)}")
            
            if results:
                result = results[0]
                print(f"Result keys: {list(result.keys())}")
                
                # Verificar diferentes possíveis chaves para dividendos
                for key in result.keys():
                    if "dividend" in key.lower() or "provento" in key.lower():
                        print(f"  - {key}: {type(result.get(key))}")
                
                dividends = result.get("dividends") or result.get("dividend") or result.get("dividendsHistory") or []
                print(f"\nDividendos encontrados: {len(dividends)}")
                
                if dividends:
                    print("\n📋 Primeiro dividendo:")
                    print(json.dumps(dividends[0], indent=2, default=str, ensure_ascii=False))
                else:
                    print("⚠️  Nenhum dividendo na chave 'dividends'")
                    print("🔍 Verificando outras chaves possíveis...")
                    for key, value in result.items():
                        if isinstance(value, list) and len(value) > 0:
                            print(f"  - {key}: lista com {len(value)} itens")
                            if len(value) > 0:
                                print(f"    Primeiro item: {json.dumps(value[0], indent=4, default=str, ensure_ascii=False)[:200]}")
        else:
            print(f"❌ Erro: Status {resp1.status_code}")
            print(f"Resposta: {resp1.text[:500]}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    # Teste 2: Sem parâmetro (para comparar)
    print(f"\n📡 Teste 2: GET https://brapi.dev/api/quote/{ticker} (sem parâmetro)")
    try:
        resp2 = requests.get(f"https://brapi.dev/api/quote/{ticker}", timeout=15)
        if resp2.status_code == 200:
            data2 = resp2.json()
            results2 = data2.get("results", [])
            if results2:
                result2 = results2[0]
                print(f"Keys disponíveis: {list(result2.keys())}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    # Testar com alguns tickers comuns
    tickers = ["PETR4", "BBSE3", "ITUB4", "VALE3"]
    for ticker in tickers:
        testar_api_dividendos(ticker)
        print("\n" + "=" * 70)

