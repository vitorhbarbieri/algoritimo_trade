# Script para facilitar o deploy online
Write-Host "Preparando deploy do Algoritimo Trade" -ForegroundColor Cyan
Write-Host ""

# Verificar se ha mudancas nao commitadas
$status = git status --porcelain
if ($status) {
    Write-Host "ATENCAO: Ha mudancas nao commitadas!" -ForegroundColor Yellow
    Write-Host "Deseja fazer commit agora? (S/N)" -ForegroundColor Yellow
    $resposta = Read-Host
    if ($resposta -eq "S" -or $resposta -eq "s") {
        Write-Host "Digite a mensagem do commit:" -ForegroundColor Cyan
        $mensagem = Read-Host
        if ([string]::IsNullOrWhiteSpace($mensagem)) {
            $mensagem = "Atualizacao para deploy"
        }
        git add .
        git commit -m $mensagem
        Write-Host "Commit realizado!" -ForegroundColor Green
    }
}

# Verificar se esta conectado ao GitHub
$remote = git remote get-url origin
if ($remote -like "*github.com*") {
    Write-Host "Repositorio conectado ao GitHub: $remote" -ForegroundColor Green
} else {
    Write-Host "ERRO: Repositorio nao esta conectado ao GitHub!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Railway (Recomendado):" -ForegroundColor Yellow
Write-Host "   -> Acesse: https://railway.app" -ForegroundColor White
Write-Host "   -> Login com GitHub" -ForegroundColor White
Write-Host "   -> New Project -> Deploy from GitHub repo" -ForegroundColor White
Write-Host "   -> Escolha: vitorhbarbieri/algoritimo_trade" -ForegroundColor White
Write-Host ""
Write-Host "2. Render (Alternativa):" -ForegroundColor Yellow
Write-Host "   -> Acesse: https://render.com" -ForegroundColor White
Write-Host "   -> Login com GitHub" -ForegroundColor White
Write-Host "   -> New + -> Web Service" -ForegroundColor White
Write-Host "   -> Conecte: vitorhbarbieri/algoritimo_trade" -ForegroundColor White
Write-Host ""
Write-Host "Dica: O deploy e automatico apos conectar o repositorio!" -ForegroundColor Cyan
Write-Host ""

# Perguntar se quer fazer push agora
Write-Host "Deseja fazer push para o GitHub agora? (S/N)" -ForegroundColor Cyan
$push = Read-Host
if ($push -eq "S" -or $push -eq "s") {
    Write-Host "Fazendo push..." -ForegroundColor Yellow
    git push origin master
    Write-Host "Push realizado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Agora va para Railway ou Render e conecte o repositorio!" -ForegroundColor Green
}
