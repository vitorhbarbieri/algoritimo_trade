# Script para configurar a API Key da OpenAI
# Execute: .\configurar_ia.ps1

Write-Host "🤖 Configuração da API Key da OpenAI" -ForegroundColor Cyan
Write-Host ""

# Verificar se já existe
$apiKey = [System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')
if ($apiKey) {
    Write-Host "⚠️  OPENAI_API_KEY já está configurada!" -ForegroundColor Yellow
    $resposta = Read-Host "Deseja sobrescrever? (s/N)"
    if ($resposta -ne 's' -and $resposta -ne 'S') {
        Write-Host "Operação cancelada." -ForegroundColor Yellow
        exit
    }
}

Write-Host "📝 Por favor, insira sua API Key da OpenAI:" -ForegroundColor Green
Write-Host "   (Você pode obter em: https://platform.openai.com/api-keys)" -ForegroundColor Gray
Write-Host ""

$novaChave = Read-Host "API Key" -AsSecureString
$chaveTexto = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($novaChave)
)

if ([string]::IsNullOrWhiteSpace($chaveTexto)) {
    Write-Host "❌ API Key não pode estar vazia!" -ForegroundColor Red
    exit 1
}

# Configurar variável de ambiente permanente
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $chaveTexto, 'User')

Write-Host ""
Write-Host "✅ API Key configurada com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Feche e reabra o terminal/PowerShell" -ForegroundColor White
Write-Host "   2. Execute o app novamente" -ForegroundColor White
Write-Host "   3. A IA estará disponível para análise de carteira" -ForegroundColor White
Write-Host ""

# Perguntar sobre o modelo
$modelo = Read-Host "Escolha o modelo (Enter para gpt-4o-mini): "
if ([string]::IsNullOrWhiteSpace($modelo)) {
    $modelo = "gpt-4o-mini"
}

[System.Environment]::SetEnvironmentVariable('OPENAI_MODEL', $modelo, 'User')
Write-Host "✅ Modelo configurado: $modelo" -ForegroundColor Green

