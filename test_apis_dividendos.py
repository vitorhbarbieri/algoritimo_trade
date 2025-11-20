#!/usr/bin/env python
"""
Script para testar diferentes APIs de dividendos
Ajuda a decidir qual API usar ou implementar como fallback
"""
import requests
import json
from datetime import datetime
import time

def testar_brapi(ticker="PETR4"):
    """Testa a API Brapi.dev (atual)"""
    print(f"\n{'='*70}")
    print(f"🔍 TESTE 1: Brapi.dev - {ticker}")
    print(f"{'='*70}")
    
    try:
        url = f"https://brapi.dev/api/quote/{ticker}?dividends=true"
        resp = requests.get(url, timeout=15)
        
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            
            if results:
                result = results[0]
                dividends_data = result.get("dividendsData", {})
                cash_dividends = dividends_data.get("cashDividends", [])
                
                print(f"✅ Sucesso! {len(cash_dividends)} dividendos encontrados")
                
                if cash_dividends:
                    print(f"\n📋 Primeiro dividendo:")
                    div = cash_dividends[0]
                    print(f"  - Data Pagamento: {div.get('paymentDate')}")
                    print(f"  - Data Ex-Dividendo: {div.get('lastDatePrior')}")
                    print(f"  - Valor: R$ {div.get('rate')}")
                    print(f"  - Tipo: {div.get('label')}")
                    return True, cash_dividends
                else:
                    print("⚠️  Nenhum dividendo em dinheiro encontrado")
                    return False, []
            else:
                print("⚠️  Nenhum resultado retornado")
                return False, []
        else:
            print(f"❌ Erro {resp.status_code}: {resp.text[:200]}")
            return False, []
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False, []

def testar_yfinance(ticker="PETR4"):
    """Testa yfinance (Yahoo Finance)"""
    print(f"\n{'='*70}")
    print(f"🔍 TESTE 2: yfinance - {ticker}")
    print(f"{'='*70}")
    
    try:
        import yfinance as yf
        
        ticker_obj = yf.Ticker(f"{ticker}.SA")
        dividends = ticker_obj.dividends
        
        if len(dividends) > 0:
            print(f"✅ Sucesso! {len(dividends)} dividendos encontrados")
            
            # Converter para formato similar ao esperado
            dividendos_formatados = []
            for data, valor in dividends.items():
                dividendos_formatados.append({
                    'data_pagamento': data.strftime('%Y-%m-%d'),
                    'data_ex_dividendo': None,  # yfinance não fornece diretamente
                    'valor_por_acao': float(valor),
                    'tipo': 'DIVIDENDO'
                })
            
            print(f"\n📋 Primeiro dividendo:")
            div = dividendos_formatados[0]
            print(f"  - Data: {div['data_pagamento']}")
            print(f"  - Valor: R$ {div['valor_por_acao']:.4f}")
            print(f"  - Data Ex-Dividendo: {div['data_ex_dividendo']} (não disponível)")
            
            # Tentar obter mais informações
            try:
                info = ticker_obj.info
                print(f"\n📊 Informações adicionais disponíveis:")
                print(f"  - Keys no info: {len(info.keys())} campos")
            except:
                pass
            
            return True, dividendos_formatados
        else:
            print("⚠️  Nenhum dividendo encontrado")
            return False, []
            
    except ImportError:
        print("❌ yfinance não está instalado. Execute: pip install yfinance")
        return False, []
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def testar_hgbrasil(ticker="PETR4"):
    """Testa HG Brasil Finance (requer API key)"""
    print(f"\n{'='*70}")
    print(f"🔍 TESTE 3: HG Brasil Finance - {ticker}")
    print(f"{'='*70}")
    
    import os
    api_key = os.getenv("HG_BRASIL_API_KEY")
    
    if not api_key:
        print("⚠️  API Key não configurada (HG_BRASIL_API_KEY)")
        print("   Para testar, configure: export HG_BRASIL_API_KEY='sua-chave'")
        return False, []
    
    try:
        # Endpoint precisa ser verificado na documentação oficial
        url = f"https://api.hgbrasil.com/finance/stock_price"
        params = {
            "key": api_key,
            "symbol": ticker
        }
        
        resp = requests.get(url, params=params, timeout=15)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Resposta recebida")
            print(f"📋 Estrutura: {json.dumps(list(data.keys())[:5], indent=2)}")
            # Verificar se há dados de dividendos na resposta
            return True, []
        else:
            print(f"❌ Erro {resp.status_code}: {resp.text[:200]}")
            return False, []
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False, []

def testar_ibovfinancials(ticker="PETR4"):
    """Testa IbovFinancials (verificar endpoint correto)"""
    print(f"\n{'='*70}")
    print(f"🔍 TESTE 4: IbovFinancials - {ticker}")
    print(f"{'='*70}")
    
    try:
        # Endpoint precisa ser verificado na documentação oficial
        # Exemplo genérico (pode não estar correto)
        url = f"https://ibovfinancials.com/api/quote/{ticker}"
        
        resp = requests.get(url, timeout=15)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Resposta recebida")
            print(f"📋 Estrutura: {json.dumps(list(data.keys())[:5], indent=2) if isinstance(data, dict) else 'Lista'}")
            return True, []
        elif resp.status_code == 404:
            print("⚠️  Endpoint não encontrado. Verificar documentação oficial.")
            return False, []
        else:
            print(f"❌ Erro {resp.status_code}: {resp.text[:200]}")
            return False, []
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False, []

def comparar_formatos(ticker="PETR4"):
    """Compara formatos de resposta das APIs"""
    print(f"\n{'='*70}")
    print(f"📊 COMPARAÇÃO DE FORMATOS - {ticker}")
    print(f"{'='*70}")
    
    resultados = {}
    
    # Testar Brapi
    sucesso, dados = testar_brapi(ticker)
    resultados['Brapi.dev'] = {
        'sucesso': sucesso,
        'dados': dados[:3] if dados else [],  # Primeiros 3
        'tem_data_ex': True if dados and dados[0].get('lastDatePrior') else False
    }
    
    time.sleep(2)  # Throttle
    
    # Testar yfinance
    sucesso, dados = testar_yfinance(ticker)
    resultados['yfinance'] = {
        'sucesso': sucesso,
        'dados': dados[:3] if dados else [],
        'tem_data_ex': False  # yfinance não fornece diretamente
    }
    
    # Resumo
    print(f"\n{'='*70}")
    print("📊 RESUMO COMPARATIVO")
    print(f"{'='*70}")
    
    for api, resultado in resultados.items():
        print(f"\n{api}:")
        print(f"  ✅ Funcionou: {resulto['sucesso']}")
        print(f"  📅 Tem data ex-dividendo: {resultado['tem_data_ex']}")
        print(f"  📊 Dividendos encontrados: {len(resultado['dados'])}")
        if resultado['dados']:
            print(f"  📋 Exemplo: {json.dumps(resultado['dados'][0], indent=4, default=str, ensure_ascii=False)[:200]}...")

if __name__ == "__main__":
    print("🧪 TESTE DE APIs DE DIVIDENDOS")
    print("=" * 70)
    
    # Testar com tickers comuns
    tickers = ["PETR4", "ITUB4", "VALE3"]
    
    for ticker in tickers:
        print(f"\n\n{'#'*70}")
        print(f"# TESTANDO COM {ticker}")
        print(f"{'#'*70}")
        
        comparar_formatos(ticker)
        time.sleep(3)  # Throttle entre tickers
    
    print(f"\n\n{'='*70}")
    print("✅ TESTES CONCLUÍDOS")
    print(f"{'='*70}")
    print("\n💡 Próximos passos:")
    print("   1. Revisar resultados acima")
    print("   2. Verificar qual API tem melhor cobertura")
    print("   3. Decidir se implementa fallback ou migra completamente")
    print("   4. Verificar custos de APIs pagas se necessário")


