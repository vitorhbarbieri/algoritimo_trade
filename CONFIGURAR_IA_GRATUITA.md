# 🆓 Configurar IA Gratuita - Guia Rápido

## 🥇 Opção 1: Google Gemini (RECOMENDADO)

### Por que escolher?
- ✅ **100% Gratuito** com generosa cota (60 req/min)
- ✅ Excelente qualidade
- ✅ Fácil de configurar
- ✅ Boa para análise financeira

### Passo a passo:

1. **Obter API Key:**
   - Acesse: https://makersuite.google.com/app/apikey
   - Faça login com sua conta Google
   - Clique em "Create API Key"
   - Copie a chave gerada

2. **Instalar biblioteca:**
   ```powershell
   pip install google-generativeai
   ```

3. **Configurar:**
   ```powershell
   setx GOOGLE_API_KEY "sua_chave_aqui"
   ```

4. **Reiniciar terminal e servidor:**
   - Feche e reabra o PowerShell
   - Reinicie o servidor Flask

5. **Pronto!** O sistema usará Gemini automaticamente.

---

## 🏠 Opção 2: Ollama (100% Local - Máxima Privacidade)

### Por que escolher?
- ✅ **100% Gratuito** e local
- ✅ **Máxima privacidade** (dados não saem do PC)
- ✅ Sem limites de requisições
- ✅ Sem necessidade de internet após instalação

### Passo a passo:

1. **Instalar Ollama:**
   - Baixe em: https://ollama.ai/download
   - Instale o executável
   - Ollama iniciará automaticamente

2. **Baixar um modelo:**
   ```powershell
   ollama pull llama2
   # ou para melhor qualidade:
   ollama pull mistral
   # ou para versão mais recente:
   ollama pull llama3
   ```

3. **Instalar biblioteca Python:**
   ```powershell
   pip install ollama
   ```

4. **Verificar se está funcionando:**
   ```powershell
   ollama list
   ```

5. **Pronto!** O sistema detectará automaticamente se Ollama estiver rodando.

**Nota:** Ollama precisa estar rodando em background. Ele inicia automaticamente com o Windows após instalação.

---

## ⚡ Opção 3: Groq (Muito Rápido)

### Por que escolher?
- ✅ **Gratuito** com boa cota
- ✅ **Muito rápido** (inferência acelerada)
- ✅ Boa qualidade

### Passo a passo:

1. **Obter API Key:**
   - Acesse: https://console.groq.com/
   - Crie uma conta ou faça login
   - Vá em "API Keys"
   - Crie uma nova chave
   - Copie a chave

2. **Instalar biblioteca:**
   ```powershell
   pip install groq
   ```

3. **Configurar:**
   ```powershell
   setx GROQ_API_KEY "sua_chave_aqui"
   ```

4. **Reiniciar terminal e servidor**

5. **Pronto!**

---

## 📊 Ordem de Prioridade do Sistema

O sistema tenta na seguinte ordem:

1. **Google Gemini** (gratuito) ← Tente primeiro!
2. **Ollama** (gratuito local)
3. **Groq** (gratuito)
4. OpenAI (pago)
5. Claude (pago)

## ✅ Testar Configuração

Execute:
```powershell
python testar_ia.py
```

Isso mostrará quais IAs estão configuradas e funcionando.

## 🎯 Recomendação Final

**Para começar rápido:** Use **Google Gemini**
- Mais fácil de configurar
- Gratuito com boa cota
- Excelente qualidade

**Para máxima privacidade:** Use **Ollama**
- 100% local
- Sem custos
- Dados nunca saem do seu PC

**Para velocidade máxima:** Use **Groq**
- Muito rápido
- Gratuito
- Boa qualidade

## 💡 Dica

Você pode configurar **múltiplas opções**! O sistema tentará automaticamente na ordem de prioridade, então se uma falhar, tentará a próxima.

