@echo off
chcp 65001 >nul
echo ========================================
echo  Enviar Relatório por Email
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python não encontrado!
    pause
    exit /b 1
)

REM Verificar se relatório existe
if not exist "RELATORIO_COMPLETO_PROJETO.md" (
    echo ❌ Relatório não encontrado!
    echo    Execute primeiro a geração do relatório.
    pause
    exit /b 1
)

echo 📧 Enviando relatório para vitorh.barbieri@gmail.com...
echo.

python enviar_relatorio_email.py vitorh.barbieri@gmail.com

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Relatório enviado com sucesso!
) else (
    echo.
    echo ❌ Erro ao enviar relatório.
    echo.
    echo 💡 DICA: Configure as variáveis de ambiente:
    echo    set EMAIL_REMETENTE=seu_email@gmail.com
    echo    set EMAIL_SENHA=sua_senha_app
    echo.
    echo    Ou edite o arquivo enviar_relatorio_email.py diretamente.
)

echo.
pause

