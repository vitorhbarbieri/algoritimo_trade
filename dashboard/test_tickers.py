"""
Teste rápido para verificar se os tickers estão sendo retornados corretamente
"""
import requests
import json

print("="*70)
print("🔍 TESTE DE TICKERS - Verificando API")
print("="*70)

try:
    # Testar endpoint de tickers
    print("\n[1/2] Testando endpoint /api/tickers...")
    response = requests.get('http://localhost:5000/api/tickers', timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        tickers = data.get('tickers', [])
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Tickers retornados: {len(tickers)}")
        print(f"\n📋 Lista de tickers:")
        for i, ticker in enumerate(tickers, 1):
            print(f"   {i}. {ticker}")
        
        # Verificar se os novos tickers estão presentes
        novos_tickers = ['BB5E3.SA', 'CMIG4.SA', 'CSMG3.SA', 'SANB11.SA', 'SYN3.SA']
        print(f"\n🔍 Verificando novos tickers:")
        for ticker in novos_tickers:
            if ticker in tickers:
                print(f"   ✅ {ticker} - PRESENTE")
            else:
                print(f"   ❌ {ticker} - AUSENTE")
    else:
        print(f"❌ Erro: Status {response.status_code}")
        print(f"Resposta: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Erro: Não foi possível conectar ao servidor")
    print("   Certifique-se de que o dashboard está rodando em http://localhost:5000")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*70)






