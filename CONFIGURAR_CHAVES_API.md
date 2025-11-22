# 🔐 Configuração Segura de Chaves de API

## ⚠️ IMPORTANTE: Segurança

**NUNCA** commite chaves de API no código! Elas foram removidas dos arquivos.

## 🔧 Como Configurar

### Opção 1: Variável de Ambiente (Recomendado)

#### Windows PowerShell:
```powershell
setx GOOGLE_API_KEY "sua_chave_aqui"
```

#### Windows CMD:
```cmd
setx GOOGLE_API_KEY "sua_chave_aqui"
```

#### Linux/Mac:
```bash
export GOOGLE_API_KEY="sua_chave_aqui"
# Para tornar permanente, adicione ao ~/.bashrc ou ~/.zshrc
```

**Importante:** Feche e reabra o terminal após configurar!

### Opção 2: Arquivo .env (Mais Conveniente)

1. **Copie o arquivo de exemplo:**
   ```powershell
   copy .env.example .env
   ```

2. **Edite o arquivo `.env`** e adicione suas chaves:
   ```
   GOOGLE_API_KEY=sua_chave_gemini_aqui
   OPENAI_API_KEY=sua_chave_openai_aqui
   ANTHROPIC_API_KEY=sua_chave_claude_aqui
   ```

3. **Instale python-dotenv** (se ainda não tiver):
   ```powershell
   pip install python-dotenv
   ```

4. **O arquivo `.env` já está no `.gitignore`** - não será commitado!

## 🔑 Onde Obter as Chaves

### Google Gemini (GRATUITO - Recomendado)
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

### OpenAI (PAGO)
1. Acesse: https://platform.openai.com/api-keys
2. Faça login
3. Clique em "Create new secret key"
4. Copie a chave (ela só aparece uma vez!)

### Anthropic Claude (PAGO)
1. Acesse: https://console.anthropic.com/
2. Faça login
3. Vá em "API Keys"
4. Crie uma nova chave

### Groq (GRATUITO)
1. Acesse: https://console.groq.com/
2. Faça login
3. Vá em "API Keys"
4. Crie uma nova chave

## ✅ Verificar Configuração

Execute:
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GOOGLE_API_KEY:', 'Configurada' if os.getenv('GOOGLE_API_KEY') else 'NAO configurada')"
```

## 🔒 Segurança

1. ✅ **NUNCA** commite arquivos `.env` no Git
2. ✅ **NUNCA** compartilhe suas chaves de API
3. ✅ **REVOGUE** chaves expostas imediatamente
4. ✅ Use variáveis de ambiente em produção
5. ✅ Regenerar chaves periodicamente

## 🚨 Se Sua Chave Foi Exposta

1. **Revogue a chave imediatamente:**
   - Gemini: https://makersuite.google.com/app/apikey
   - OpenAI: https://platform.openai.com/api-keys
   - Claude: https://console.anthropic.com/

2. **Gere uma nova chave**

3. **Configure a nova chave** usando uma das opções acima

4. **Remova do histórico do Git** (se necessário):
   ```powershell
   git filter-branch --force --index-filter "git rm --cached --ignore-unmatch arquivo_com_chave.py" --prune-empty --tag-name-filter cat -- --all
   ```

## 📝 Arquivos Atualizados

Os seguintes arquivos foram corrigidos para não conter chaves hardcoded:
- ✅ `reiniciar_servidor.py`
- ✅ `iniciar_servidor.ps1`
- ✅ `iniciar_com_auth.ps1`
- ✅ `dashboard/app.py` (agora carrega .env)

Todos os scripts agora leem de variáveis de ambiente ou arquivo `.env`.

