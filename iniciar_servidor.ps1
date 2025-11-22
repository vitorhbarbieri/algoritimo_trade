# Script simples para iniciar servidor Flask
Write-Host "`n=== INICIANDO SERVIDOR ===" -ForegroundColor Green

# Configurar Gemini
$env:GOOGLE_API_KEY = "AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI"

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

