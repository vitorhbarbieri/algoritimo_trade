"""
Script Python para reiniciar servidor Flask limpo
"""
import os
import sys
import subprocess
import time
import signal

print("\n" + "="*70)
print("=== LIMPANDO E REINICIANDO SERVIDOR ===")
print("="*70)

# 1. Matar processos Python rodando app.py
print("\n1. Encerrando processos Python do Flask...")
try:
    if sys.platform == "win32":
        # Windows
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True,
            text=True
        )
        if "python.exe" in result.stdout:
            subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                         capture_output=True, stderr=subprocess.DEVNULL)
            time.sleep(2)
            print("   ✅ Processos encerrados")
        else:
            print("   ℹ️  Nenhum processo encontrado")
    else:
        # Linux/Mac
        subprocess.run(["pkill", "-f", "app.py"], 
                     capture_output=True, stderr=subprocess.DEVNULL)
        time.sleep(2)
        print("   ✅ Processos encerrados")
except Exception as e:
    print(f"   ⚠️  Erro ao encerrar processos: {e}")

# 2. Limpar cache Python
print("\n2. Limpando cache Python...")
import shutil
cache_dirs = []
for root, dirs, files in os.walk("."):
    if "__pycache__" in dirs:
        cache_path = os.path.join(root, "__pycache__")
        cache_dirs.append(cache_path)
    for file in files:
        if file.endswith(".pyc"):
            try:
                os.remove(os.path.join(root, file))
            except:
                pass

for cache_dir in cache_dirs:
    try:
        shutil.rmtree(cache_dir)
    except:
        pass

print(f"   ✅ Cache limpo ({len(cache_dirs)} diretórios)")

# 3. Configurar Gemini
print("\n3. Configurando Google Gemini...")
os.environ["GOOGLE_API_KEY"] = "AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI"
print("   ✅ GOOGLE_API_KEY configurada")

# 4. Verificar dependências
print("\n4. Verificando dependências...")
try:
    import google.generativeai
    print("   ✅ google-generativeai instalado")
except ImportError:
    print("   ⚠️  Instalando google-generativeai...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "google-generativeai"])
    print("   ✅ Instalado")

# 5. Iniciar servidor
print("\n" + "="*70)
print("=== SERVIDOR INICIANDO ===")
print("="*70)
print("\nURL: http://localhost:5000")
print("\nCREDENCIAIS:")
print("  admin@algoritimo.com / admin123")
print("  OU")
print("  vitorh.barbieri@gmail.com / vitor123")
print("\nIA: Google Gemini (GRATUITO) - Ativo")
print("\nPressione Ctrl+C para parar\n")

# Mudar para diretório dashboard e iniciar
os.chdir("dashboard")
os.execv(sys.executable, [sys.executable, "app.py"])

