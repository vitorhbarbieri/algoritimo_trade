"""Script para testar o app Flask e identificar erros"""
import sys
import os
import traceback

print("="*70)
print("Testando imports e configuração do Flask...")
print("="*70)

# Testar Flask
try:
    from flask import Flask
    print("✅ Flask importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar Flask: {e}")
    print("Execute: pip install flask")
    sys.exit(1)

# Testar imports do app
print("\nTestando imports do app...")
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

try:
    from dashboard.app import app
    print("✅ App importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar app: {e}")
    traceback.print_exc()
    sys.exit(1)

# Verificar templates
print("\nVerificando templates...")
template_dir = os.path.join(base_dir, 'dashboard', 'templates')
if os.path.exists(template_dir):
    print(f"✅ Diretório de templates encontrado: {template_dir}")
    templates = os.listdir(template_dir)
    print(f"   Templates encontrados: {templates}")
else:
    print(f"❌ Diretório de templates não encontrado: {template_dir}")

# Testar rota
print("\nTestando rota principal...")
try:
    with app.test_client() as client:
        response = client.get('/')
        print(f"✅ Rota '/' retornou status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Resposta: {response.data[:200]}")
except Exception as e:
    print(f"❌ Erro ao testar rota: {e}")
    traceback.print_exc()

print("\n" + "="*70)
print("Teste concluído!")
print("="*70)

