# Script simples para iniciar servidor Flask
Write-Host "`n=== INICIANDO SERVIDOR ===" -ForegroundColor Green

# Configurar Gemini (lê de variável de ambiente)
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "AVISO: GOOGLE_API_KEY nao configurada!" -ForegroundColor Yellow
    Write-Host "Configure: setx GOOGLE_API_KEY sua_chave_aqui" -ForegroundColor White
    Write-Host "Ou crie arquivo .env com: GOOGLE_API_KEY=sua_chave_aqui" -ForegroundColor White
    exit 1
}

# Instalar dependências
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -q google-generativeai flask flask-login werkzeug openpyxl 2>&1 | Out-Null

Write-Host "`n=== SERVIDOR INICIANDO ===" -ForegroundColor Green
Write-Host "URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "`nCREDENCIAIS:" -ForegroundColor Yellow
Write-Host "  admin@algoritimo.com / admin123" -ForegroundColor White
Write-Host "  OU" -ForegroundColor Gray
Write-Host "  vitorh.barbieri@gmail.com / vitor123" -ForegroundColor White
Write-Host "`nIA: Google Gemini (GRATUITO) - Configurado" -ForegroundColor Green
Write-Host "`nPressione Ctrl+C para parar`n" -ForegroundColor Gray

cd dashboard
python app.py

