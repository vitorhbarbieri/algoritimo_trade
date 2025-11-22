"""Script para iniciar o servidor Flask com tratamento de erros"""
import sys
import os
import traceback

print("="*70)
print("Iniciando servidor Flask...")
print("="*70)

try:
    # Verificar se Flask está instalado
    import flask
    print(f"✅ Flask {flask.__version__} instalado")
except ImportError:
    print("❌ Flask não está instalado!")
    print("Execute: pip install flask")
    sys.exit(1)

# Mudar para o diretório do projeto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    # Importar e iniciar o app
    from dashboard.app import app
    
    print("\n✅ App carregado com sucesso")
    print("\n" + "="*70)
    print("Servidor iniciando...")
    print("Acesse: http://localhost:5000")
    print("="*70)
    print("\nPressione Ctrl+C para parar\n")
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n⚠️  Servidor interrompido pelo usuário")
except Exception as e:
    print(f"\n❌ Erro ao iniciar servidor:")
    print(f"   {str(e)}")
    print("\nTraceback completo:")
    traceback.print_exc()
    sys.exit(1)

