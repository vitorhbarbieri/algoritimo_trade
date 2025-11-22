# Script para atualizar servidor e garantir que usa código mais recente
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Atualizando Servidor Flask" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Limpar cache Python
Write-Host "Limpando cache Python..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "Cache limpo!" -ForegroundColor Green
Write-Host ""

# Verificar processos Python rodando
Write-Host "Verificando processos Python..." -ForegroundColor Yellow
$processos = Get-Process python -ErrorAction SilentlyContinue
if ($processos) {
    Write-Host "ATENCAO: Encontrados $($processos.Count) processo(s) Python rodando!" -ForegroundColor Red
    Write-Host "Pare o servidor Flask (Ctrl+C) antes de continuar." -ForegroundColor Yellow
    Write-Host ""
    $continuar = Read-Host "Deseja continuar mesmo assim? (S/N)"
    if ($continuar -ne "S" -and $continuar -ne "s") {
        Write-Host "Cancelado." -ForegroundColor Yellow
        exit
    }
} else {
    Write-Host "Nenhum processo Python encontrado." -ForegroundColor Green
}
Write-Host ""

# Verificar correções
Write-Host "Verificando correcoes de dividendos..." -ForegroundColor Yellow
$ibovDesabilitada = Select-String -Path "data\dividendos_collector.py" -Pattern "IbovFinancials esta temporariamente desabilitada" -Quiet
$fallbackCorreto = Select-String -Path "data\dividendos_collector.py" -Pattern "fontes_preferidas = \['brapi', 'yfinance'\]" -Quiet

if ($ibovDesabilitada -and $fallbackCorreto) {
    Write-Host "CORRECOES APLICADAS:" -ForegroundColor Green
    Write-Host "  - IbovFinancials desabilitada" -ForegroundColor Green
    Write-Host "  - Fallback: ['brapi', 'yfinance']" -ForegroundColor Green
} else {
    Write-Host "ATENCAO: Algumas correcoes podem nao estar aplicadas!" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pronto para reiniciar servidor!" -ForegroundColor Green
Write-Host "Execute: python dashboard/app.py" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

