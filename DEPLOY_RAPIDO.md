# 🚀 Deploy Rápido - Algoritimo Trade

## Opção 1: Railway (Recomendado - Mais Fácil) ⚡

### Passo a Passo:

1. **Acesse:** https://railway.app
2. **Clique em "Login"** e faça login com sua conta GitHub (`vitorh.barbieri`)
3. **Clique em "New Project"**
4. **Selecione "Deploy from GitHub repo"**
5. **Autorize Railway** a acessar seus repositórios (se necessário)
6. **Escolha o repositório:** `vitorhbarbieri/algoritimo_trade`
7. **Railway detecta automaticamente** o projeto Python e configura tudo!
8. **Aguarde o deploy** (2-3 minutos)
9. **Pronto!** 🎉 Você receberá uma URL como: `https://algoritimo-trade-production.up.railway.app`

### Variáveis de Ambiente (Opcional):
Se quiser melhorar performance, adicione no Railway:
- `BRAPI_TOKEN` - Token da API Brapi.dev (opcional)
- `IBOVFINANCIALS_TOKEN` - Token da API IbovFinancials (opcional)

**Como adicionar variáveis:**
1. No projeto Railway, clique em "Variables"
2. Adicione cada variável com seu valor
3. O Railway reinicia automaticamente

---

## Opção 2: Render (Alternativa Gratuita) 🌐

### Passo a Passo:

1. **Acesse:** https://render.com
2. **Faça login** com GitHub
3. **Clique em "New +" → "Web Service"**
4. **Conecte o repositório:** `vitorhbarbieri/algoritimo_trade`
5. **Configure:**
   - **Name:** `algoritimo-trade`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python dashboard/app.py`
6. **Clique em "Create Web Service"**
7. **Aguarde o deploy** (3-5 minutos)
8. **Pronto!** 🎉 URL: `https://algoritimo-trade.onrender.com`

---

## ✅ Verificação Pós-Deploy

Após o deploy, teste:

1. **Acesse a URL** fornecida pelo serviço
2. **Verifique se o dashboard carrega**
3. **Teste a análise de um ticker** (ex: ITUB4)
4. **Verifique os logs** no painel do serviço se houver problemas

---

## 🔄 Atualizações Automáticas

Ambos os serviços fazem deploy automático quando você faz `git push`:

```bash
git add .
git commit -m "Sua atualização"
git push
# Deploy automático em alguns minutos!
```

---

## 🐛 Problemas Comuns

### App não inicia:
- Verifique os logs no painel do serviço
- Certifique-se que `dashboard/app.py` está correto

### Erro de módulo não encontrado:
- Verifique se `requirements.txt` está completo
- Veja os logs de build no painel

### Timeout:
- Render pode ter timeout em 30 segundos se não houver tráfego
- Railway não tem esse problema

---

## 📊 Status do Projeto

✅ **Configurado para produção:**
- ✅ Usa variável `PORT` do ambiente
- ✅ Host `0.0.0.0` configurado
- ✅ Debug desabilitado em produção
- ✅ Procfile configurado
- ✅ railway.json configurado
- ✅ render.yaml configurado

---

**Última atualização:** Janeiro 2025

