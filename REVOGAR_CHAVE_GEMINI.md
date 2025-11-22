# 🚨 AÇÃO URGENTE: Revogar Chave Gemini Exposta

## ⚠️ Sua chave da API do Gemini foi exposta no GitHub!

Você precisa **REVOGAR** a chave imediatamente e criar uma nova.

## 🔴 Passos Urgentes:

### 1. Revogar Chave Exposta (FAÇA AGORA!)

1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Encontre a chave: `AIzaSyB3gUgY_UyF3sWfDdpJkD5y-UKG0qXfkLI`
4. Clique em **"Delete"** ou **"Revoke"**
5. Confirme a revogação

### 2. Criar Nova Chave

1. Na mesma página, clique em **"Create API Key"**
2. Copie a nova chave gerada
3. **NÃO compartilhe esta chave!**

### 3. Configurar Nova Chave Localmente

#### Opção A: Variável de Ambiente (Recomendado)
```powershell
setx GOOGLE_API_KEY "sua_nova_chave_aqui"
```
**Feche e reabra o terminal!**

#### Opção B: Arquivo .env
1. Copie `.env.example` para `.env`:
   ```powershell
   copy .env.example .env
   ```

2. Edite `.env` e adicione:
   ```
   GOOGLE_API_KEY=sua_nova_chave_aqui
   ```

3. Instale python-dotenv:
   ```powershell
   pip install python-dotenv
   ```

### 4. Verificar

```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OK' if os.getenv('GOOGLE_API_KEY') else 'NAO CONFIGURADA')"
```

## ✅ Correções Aplicadas

- ✅ Chaves removidas de todos os arquivos de código
- ✅ Scripts atualizados para ler de variáveis de ambiente
- ✅ Arquivo `.env.example` criado como template
- ✅ `.env` adicionado ao `.gitignore`
- ✅ Documentação de segurança criada

## 📋 Próximos Passos

1. ✅ Revogar chave exposta (URGENTE!)
2. ✅ Criar nova chave
3. ✅ Configurar localmente (variável de ambiente ou .env)
4. ✅ Testar o sistema
5. ✅ Considerar regenerar outras chaves também (por segurança)

## 🔒 Boas Práticas

- ✅ **NUNCA** commite chaves no código
- ✅ Use variáveis de ambiente ou arquivo `.env`
- ✅ Mantenha `.env` no `.gitignore`
- ✅ Revogue chaves expostas imediatamente
- ✅ Regenerar chaves periodicamente

