# Script para iniciar o servidor Flask no localhost
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando Algoritimo Trade - Localhost" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Flask esta instalado
Write-Host "Verificando dependencias..." -ForegroundColor Yellow
try {
    $flask = python -c "import flask; print(flask.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Flask instalado: $flask" -ForegroundColor Green
    } else {
        Write-Host "Flask nao encontrado. Instalando..." -ForegroundColor Yellow
        pip install flask -q
    }
} catch {
    Write-Host "Instalando Flask..." -ForegroundColor Yellow
    pip install flask -q
}

Write-Host ""
Write-Host "Iniciando servidor Flask..." -ForegroundColor Green
Write-Host ""
Write-Host "O servidor estara disponivel em:" -ForegroundColor Cyan
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host "  http://127.0.0.1:5000" -ForegroundColor White
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar o servidor
python dashboard/app.py

