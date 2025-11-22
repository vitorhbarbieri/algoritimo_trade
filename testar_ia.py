"""Script para testar conexão com IA"""
import os
import sys
sys.path.insert(0, '.')

print("="*70)
print("TESTE DE CONEXÃO COM IA")
print("="*70)

# Verificar variáveis de ambiente
print("\n1. Verificando variáveis de ambiente...")
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

print(f"   OPENAI_API_KEY: {'[OK] Configurada' if openai_key else '[ERRO] Nao configurada'}")
print(f"   ANTHROPIC_API_KEY: {'[OK] Configurada' if anthropic_key else '[ERRO] Nao configurada'}")

# Verificar bibliotecas
print("\n2. Verificando bibliotecas...")
try:
    import openai
    print(f"   [OK] openai instalado (versao: {getattr(openai, '__version__', 'N/A')})")
    print(f"   [OK] Cliente OpenAI disponivel: {hasattr(openai, 'OpenAI')}")
except ImportError:
    print("   [ERRO] openai NAO instalado")
    openai = None

try:
    import anthropic
    print(f"   [OK] anthropic instalado")
except ImportError:
    print("   [ERRO] anthropic NAO instalado")
    anthropic = None

# Testar chamada OpenAI
print("\n3. Testando chamada OpenAI...")
if openai_key and openai:
    try:
        from core.ia_advisor import _chamar_openai
        prompt_teste = "Responda apenas: {'teste': 'ok'}"
        resultado = _chamar_openai(prompt_teste)
        print(f"   [OK] OpenAI funcionando!")
        print(f"   Resposta: {str(resultado)[:100]}")
    except Exception as e:
        print(f"   [ERRO] Erro ao chamar OpenAI: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("   ⚠️  OpenAI não disponível (falta API key ou biblioteca)")

# Testar chamada Claude
print("\n4. Testando chamada Claude...")
if anthropic_key and anthropic:
    try:
        from core.ia_advisor import _chamar_claude
        prompt_teste = "Responda apenas: {'teste': 'ok'}"
        resultado = _chamar_claude(prompt_teste)
        print(f"   [OK] Claude funcionando!")
        print(f"   Resposta: {str(resultado)[:100]}")
    except Exception as e:
        print(f"   [ERRO] Erro ao chamar Claude: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("   ⚠️  Claude não disponível (falta API key ou biblioteca)")

print("\n" + "="*70)

