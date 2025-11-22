"""Testar modelos disponíveis do Gemini"""
import os
os.environ['GOOGLE_API_KEY'] = 'AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI'

try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    
    print("="*70)
    print("TESTANDO MODELOS GEMINI")
    print("="*70)
    
    # Listar modelos disponíveis
    print("\nModelos disponíveis:")
    models = list(genai.list_models())
    modelos_geracao = [m for m in models if 'generateContent' in m.supported_generation_methods]
    
    for m in modelos_geracao[:10]:
        print(f"  - {m.name}")
    
    # Testar modelos
    modelos_tentar = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    print("\n" + "="*70)
    print("TESTANDO MODELOS")
    print("="*70)
    
    for modelo_nome in modelos_tentar:
        try:
            print(f"\nTestando {modelo_nome}...")
            model = genai.GenerativeModel(modelo_nome)
            response = model.generate_content("Responda apenas: OK")
            print(f"  ✅ {modelo_nome} FUNCIONOU!")
            print(f"  Resposta: {response.text[:50]}")
            print(f"\n✅ MODELO RECOMENDADO: {modelo_nome}")
            break
        except Exception as e:
            print(f"  ❌ {modelo_nome} falhou: {str(e)[:100]}")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()

