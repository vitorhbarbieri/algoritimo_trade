# Script para derrubar todas as instâncias do Flask e reiniciar limpo
Write-Host "`n=== LIMPANDO INSTANCIAS ANTIGAS ===" -ForegroundColor Yellow

# 1. Matar todos os processos Python rodando app.py
Write-Host "`n1. Encerrando processos Python do Flask..." -ForegroundColor Cyan
$processos = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*app.py*" -or $_.Path -like "*python*"
}

if ($processos) {
    foreach ($proc in $processos) {
        try {
            Write-Host "   Encerrando processo PID: $($proc.Id)" -ForegroundColor Gray
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        } catch {
            # Ignorar erros
        }
    }
    Start-Sleep -Seconds 2
    Write-Host "   Processos encerrados" -ForegroundColor Green
} else {
    Write-Host "   Nenhum processo encontrado" -ForegroundColor Gray
}

# 2. Limpar cache Python
Write-Host "`n2. Limpando cache Python..." -ForegroundColor Cyan
Get-ChildItem -Path . -Recurse -Filter __pycache__ -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "   Cache limpo" -ForegroundColor Green

# 3. Verificar porta 5000
Write-Host "`n3. Verificando porta 5000..." -ForegroundColor Cyan
$porta5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($porta5000) {
    Write-Host "   Porta 5000 em uso, tentando liberar..." -ForegroundColor Yellow
    $processoPorta = Get-Process -Id ($porta5000.OwningProcess) -ErrorAction SilentlyContinue
    if ($processoPorta) {
        Stop-Process -Id $processoPorta.Id -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }
    Write-Host "   Porta liberada" -ForegroundColor Green
} else {
    Write-Host "   Porta 5000 livre" -ForegroundColor Green
}

# 4. Configurar Gemini
Write-Host "`n4. Configurando Google Gemini..." -ForegroundColor Cyan
$env:GOOGLE_API_KEY = "AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI"
Write-Host "   GOOGLE_API_KEY configurada" -ForegroundColor Green

# 5. Instalar dependências
Write-Host "`n5. Verificando dependencias..." -ForegroundColor Cyan
pip install -q google-generativeai flask flask-login werkzeug openpyxl 2>&1 | Out-Null
Write-Host "   Dependencias OK" -ForegroundColor Green

# 6. Iniciar servidor limpo
Write-Host "`n=== INICIANDO SERVIDOR LIMPO ===" -ForegroundColor Green
Write-Host "`nURL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "`nCREDENCIAIS:" -ForegroundColor Yellow
Write-Host "  admin@algoritimo.com / admin123" -ForegroundColor White
Write-Host "  OU" -ForegroundColor Gray
Write-Host "  vitorh.barbieri@gmail.com / vitor123" -ForegroundColor White
Write-Host "`nIA: Google Gemini (GRATUITO) - Ativo" -ForegroundColor Green
Write-Host "`nPressione Ctrl+C para parar`n" -ForegroundColor Gray

cd dashboard
python app.py

