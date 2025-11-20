# Script para verificar e ajudar a instalar Node.js
# Execute: .\instalar_nodejs.ps1

Write-Host "🔍 Verificando Node.js..." -ForegroundColor Cyan

# Verificar se Node.js está instalado
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✅ Node.js instalado!" -ForegroundColor Green
    Write-Host "   Versão Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "   Versão npm: $npmVersion" -ForegroundColor Green
    Write-Host "`n✅ Pronto para instalar BMAD!" -ForegroundColor Green
    Write-Host "`nExecute: npx bmad-method install" -ForegroundColor Yellow
} catch {
    Write-Host "❌ Node.js não está instalado!" -ForegroundColor Red
    Write-Host "`n📥 Para instalar:" -ForegroundColor Yellow
    Write-Host "   1. Acesse: https://nodejs.org/" -ForegroundColor White
    Write-Host "   2. Baixe a versão LTS (recomendada)" -ForegroundColor White
    Write-Host "   3. Execute o instalador" -ForegroundColor White
    Write-Host "   4. Marque todas as opções durante instalação" -ForegroundColor White
    Write-Host "   5. Reinicie o terminal" -ForegroundColor White
    Write-Host "   6. Execute este script novamente" -ForegroundColor White
    
    Write-Host "`n💡 Ou abra o link diretamente:" -ForegroundColor Cyan
    Write-Host "   https://nodejs.org/" -ForegroundColor Blue
    
    # Tentar abrir o navegador
    try {
        Start-Process "https://nodejs.org/"
        Write-Host "`n🌐 Abrindo página de download..." -ForegroundColor Green
    } catch {
        Write-Host "`n⚠️  Não foi possível abrir o navegador automaticamente" -ForegroundColor Yellow
    }
}


