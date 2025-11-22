# 🔧 Solução para Erros de IA

## ❌ Erro: "429 Too Many Requests" / "insufficient_quota"

### Problema
A conta OpenAI está sem créditos ou atingiu o limite de taxa.

### Soluções

#### Opção 1: Adicionar Créditos na OpenAI (Recomendado)
1. Acesse: https://platform.openai.com/account/billing
2. Adicione créditos ao seu plano
3. Aguarde alguns minutos para a atualização
4. Tente novamente

#### Opção 2: Configurar Claude (Anthropic) como Alternativa
1. Acesse: https://console.anthropic.com/
2. Crie uma conta ou faça login
3. Gere uma API Key
4. Configure no Windows PowerShell:
   ```powershell
   setx ANTHROPIC_API_KEY "sua_chave_aqui"
   ```
5. Feche e reabra o terminal
6. Reinicie o servidor Flask

#### Opção 3: Aguardar Rate Limit
- Se for apenas rate limit (não quota), aguarde 1-5 minutos
- O sistema já tem retry automático com backoff exponencial

## 🔄 Melhorias Implementadas

### 1. Retry Automático
- ✅ Sistema tenta novamente automaticamente em caso de rate limit
- ✅ Backoff exponencial (1s, 2s, 4s...)
- ✅ Até 3 tentativas antes de falhar

### 2. Mensagens de Erro Melhoradas
- ✅ Mensagens mais claras e acionáveis
- ✅ Instruções passo a passo para resolver
- ✅ Links diretos para configuração

### 3. Tratamento de Erros Específicos
- ✅ Detecta quota insuficiente
- ✅ Detecta rate limit
- ✅ Detecta problemas de autenticação
- ✅ Fornece soluções específicas para cada caso

## 📋 Verificar Status das APIs

Execute o script de teste:
```powershell
python testar_ia.py
```

Isso mostrará:
- ✅ Se as API keys estão configuradas
- ✅ Se as bibliotecas estão instaladas
- ✅ Se as APIs estão funcionando
- ❌ Qual erro específico está ocorrendo

## 🚀 Configuração Rápida

### Para OpenAI:
```powershell
# 1. Obter API key em: https://platform.openai.com/api-keys
# 2. Configurar:
setx OPENAI_API_KEY "sk-..."

# 3. Verificar:
python -c "import os; print('OK' if os.getenv('OPENAI_API_KEY') else 'NAO CONFIGURADA')"
```

### Para Claude:
```powershell
# 1. Obter API key em: https://console.anthropic.com/
# 2. Configurar:
setx ANTHROPIC_API_KEY "sk-ant-..."

# 3. Instalar biblioteca:
pip install anthropic

# 4. Verificar:
python -c "import os; print('OK' if os.getenv('ANTHROPIC_API_KEY') else 'NAO CONFIGURADA')"
```

## ⚠️ Erros Comuns

### "insufficient_quota"
**Causa:** Sem créditos na conta OpenAI  
**Solução:** Adicionar créditos em https://platform.openai.com/account/billing

### "429 Too Many Requests"
**Causa:** Rate limit atingido  
**Solução:** Aguardar alguns minutos (sistema tenta automaticamente)

### "ANTHROPIC_API_KEY não configurada"
**Causa:** Claude não está configurado  
**Solução:** Configurar ANTHROPIC_API_KEY ou usar apenas OpenAI

### "Biblioteca openai não instalada"
**Causa:** Biblioteca não instalada  
**Solução:** `pip install openai`

### "Biblioteca anthropic não instalada"
**Causa:** Biblioteca não instalada  
**Solução:** `pip install anthropic`

## 🔍 Debug

Para ver logs detalhados, verifique o console do servidor Flask. Os logs mostram:
- Tentativas de chamada
- Erros específicos
- Retries automáticos
- Mensagens de sucesso

## 📞 Próximos Passos

1. **Se OpenAI sem créditos:**
   - Adicione créditos OU
   - Configure Claude como alternativa

2. **Se ambas falharem:**
   - Verifique se as API keys estão corretas
   - Verifique se as bibliotecas estão instaladas
   - Execute `python testar_ia.py` para diagnóstico

3. **Sistema funcionando:**
   - O sistema tentará automaticamente em caso de rate limit
   - Mensagens de erro serão mais claras
   - Você saberá exatamente o que fazer

