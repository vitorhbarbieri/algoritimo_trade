@echo off
chcp 65001 >nul
echo ========================================
echo  Sistema de Trading - Acesso Remoto
echo ========================================
echo.

REM Verificar se ngrok está instalado
where ngrok >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ ngrok não encontrado!
    echo.
    echo 📥 Instale o ngrok:
    echo    1. Baixe de https://ngrok.com/download
    echo    2. Ou use: choco install ngrok
    echo    3. Configure seu token: ngrok config add-authtoken SEU_TOKEN
    echo.
    pause
    exit /b 1
)

REM Verificar se Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python não encontrado!
    pause
    exit /b 1
)

echo ✅ Dependências verificadas
echo.

REM Iniciar API Server
echo [1/4] Iniciando API Server...
start "API Server - Porta 5000" cmd /k "title API Server && python api_server.py"
timeout /t 3 /nobreak >nul

REM Iniciar Dashboard
echo [2/4] Iniciando Dashboard...
start "Dashboard - Porta 8501" cmd /k "title Dashboard && streamlit run dashboard_central.py --server.port 8501"
timeout /t 5 /nobreak >nul

REM Iniciar ngrok para API
echo [3/4] Iniciando ngrok para API (porta 5000)...
start "ngrok API" cmd /k "title ngrok API && ngrok http 5000"
timeout /t 2 /nobreak >nul

REM Iniciar ngrok para Dashboard
echo [4/4] Iniciando ngrok para Dashboard (porta 8501)...
start "ngrok Dashboard" cmd /k "title ngrok Dashboard && ngrok http 8501"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo  ✅ Sistema Iniciado com Sucesso!
echo ========================================
echo.
echo 📊 Acesso Local:
echo    Dashboard: http://localhost:8501
echo    API:       http://localhost:5000
echo.
echo 🌐 Acesso Remoto:
echo    1. Abra http://localhost:4040 no navegador
echo    2. Você verá as URLs públicas do ngrok
echo    3. Use essas URLs para acessar de qualquer lugar
echo.
echo ⚠️  IMPORTANTE:
echo    - As URLs do ngrok mudam a cada reinício (versão gratuita)
echo    - Para URL permanente, use Cloudflare Tunnel (ver configurar_acesso_remoto.md)
echo.
echo 🛑 Para parar o sistema, feche todas as janelas abertas
echo.
pause

