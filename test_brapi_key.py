#!/usr/bin/env python
"""Testa a API Brapi.dev com a chave configurada"""
import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

api_key = os.getenv("BRAPI_API_KEY")
print(f"\n🔑 API Key configurada: {'Sim' if api_key else 'Não'}")
if api_key:
    print(f"   Chave: {api_key[:10]}...{api_key[-4:]}")
else:
    print("   ⚠️  Chave não encontrada no .env")

print("\n" + "="*70)
print("🧪 Testando API com tickers que antes davam erro 401...")
print("="*70)

import requests

tickers_teste = ["BBSE3", "PETR4"]

for ticker in tickers_teste:
    print(f"\n📊 Testando {ticker}...")
    
    url = f"https://brapi.dev/api/quote/{ticker}?dividends=true"
    if api_key:
        url += f"&token={api_key}"
    
    try:
        resp = requests.get(url, timeout=15)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                result = results[0]
                dividends_data = result.get("dividendsData", {})
                cash_dividends = dividends_data.get("cashDividends", [])
                print(f"   ✅ Sucesso! {len(cash_dividends)} dividendos encontrados")
                if cash_dividends:
                    print(f"   📅 Último: {cash_dividends[0].get('paymentDate', 'N/A')} - R$ {cash_dividends[0].get('rate', 0):.4f}")
            else:
                print("   ⚠️  Nenhum resultado")
        elif resp.status_code == 401:
            print(f"   ❌ 401 Unauthorized - Ticker ainda não disponível mesmo com API key")
        else:
            print(f"   ⚠️  Erro: {resp.status_code}")
            print(f"   Resposta: {resp.text[:200]}")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:100]}")

print("\n" + "="*70)
print("✅ Teste concluído!")

