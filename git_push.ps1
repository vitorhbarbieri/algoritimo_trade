# Script PowerShell para facilitar commits e push para GitHub
# Uso: .\git_push.ps1 "Mensagem do commit"

param(
    [Parameter(Mandatory=$true)]
    [string]$Mensagem
)

Write-Host "🔄 Preparando commit..." -ForegroundColor Cyan

# Verificar status
Write-Host "`n📊 Status do repositório:" -ForegroundColor Yellow
git status

# Adicionar todos os arquivos
Write-Host "`n➕ Adicionando arquivos..." -ForegroundColor Cyan
git add .

# Fazer commit
Write-Host "`n💾 Fazendo commit..." -ForegroundColor Cyan
git commit -m $Mensagem

# Verificar se há remote configurado
$remote = git remote -v
if ($remote -match "origin") {
    Write-Host "`n🚀 Enviando para GitHub..." -ForegroundColor Cyan
    git push
    
    Write-Host "`n✅ Concluído! Código enviado para GitHub." -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Remote 'origin' não configurado!" -ForegroundColor Yellow
    Write-Host "Execute: git remote add origin https://github.com/SEU_USUARIO/algoritimo-trade.git" -ForegroundColor Yellow
    Write-Host "Veja GITHUB_SETUP.md para mais detalhes." -ForegroundColor Yellow
}


