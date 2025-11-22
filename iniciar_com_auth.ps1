# Script para iniciar o servidor Flask com autenticação multi-tenant
Write-Host "`n=== INICIANDO SERVIDOR COM AUTENTICACAO ===" -ForegroundColor Green
Write-Host ""

# Verificar se está no diretório correto
if (-not (Test-Path "dashboard\app.py")) {
    Write-Host "ERRO: Execute este script na raiz do projeto!" -ForegroundColor Red
    exit 1
}

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "ERRO: Python nao encontrado! Instale Python primeiro." -ForegroundColor Red
    exit 1
}

# Instalar dependências se necessário
Write-Host "`nVerificando dependencias..." -ForegroundColor Yellow
pip install -q flask flask-login werkzeug google-generativeai 2>&1 | Out-Null

# Configurar Google Gemini
Write-Host "Configurando Google Gemini..." -ForegroundColor Yellow
$env:GOOGLE_API_KEY = "AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI"
Write-Host "GOOGLE_API_KEY configurada para esta sessao" -ForegroundColor Green

# Executar migração se necessário
Write-Host "Verificando migracao do banco de dados..." -ForegroundColor Yellow
python data/migrate_multi_tenant.py 2>&1 | Out-Null

Write-Host "`n=== SERVIDOR INICIANDO ===" -ForegroundColor Green
Write-Host "Acesse: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "CREDENCIAIS PADRAO:" -ForegroundColor Yellow
Write-Host "  Email: admin@algoritimo.com" -ForegroundColor White
Write-Host "  Senha: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Ou: vitorh.barbieri@gmail.com / vitor123" -ForegroundColor White
Write-Host ""
Write-Host "IA CONFIGURADA:" -ForegroundColor Green
Write-Host "  Google Gemini (GRATUITO) - Ativo" -ForegroundColor White
Write-Host ""
Write-Host "Ou crie uma nova conta em: http://localhost:5000/auth/register" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Gray
Write-Host ""

# Iniciar servidor Flask com Gemini configurado
cd dashboard
$env:GOOGLE_API_KEY = "AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI"
python app.py

