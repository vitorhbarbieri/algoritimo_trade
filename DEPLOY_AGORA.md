# 🚀 Deploy Rápido - Colocar Online AGORA

## Opção 1: Railway (Recomendado - Mais Rápido) ⚡

### Passos:

1. **Acesse:** https://railway.app
2. **Clique em "Login"** e faça login com GitHub
3. **Clique em "New Project"**
4. **Selecione "Deploy from GitHub repo"**
5. **Escolha:** `vitorhbarbieri/algoritimo_trade`
6. **Railway detecta automaticamente** e faz o deploy!
7. **Aguarde 2-3 minutos**
8. **Pronto!** 🎉 Você receberá uma URL como: `https://algoritimo-trade-production.up.railway.app`

### Variáveis de Ambiente (Opcional):
No Railway, vá em "Variables" e adicione:
- `BRAPI_TOKEN` (se tiver)
- `IBOVFINANCIALS_TOKEN` (se tiver)

---

## Opção 2: Render (Alternativa Gratuita) 🌐

### Passos:

1. **Acesse:** https://render.com
2. **Faça login** com GitHub
3. **Clique em "New +" → "Web Service"**
4. **Conecte:** `vitorhbarbieri/algoritimo_trade`
5. **Configure:**
   - **Name:** `algoritimo-trade`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python dashboard/app.py`
6. **Clique em "Create Web Service"**
7. **Aguarde 3-5 minutos**
8. **Pronto!** 🎉 URL: `https://algoritimo-trade.onrender.com`

---

## ✅ Testar Após Deploy

1. Acesse a URL fornecida
2. Verifique se o dashboard carrega
3. Selecione um ticker (ex: ITUB4) e clique para analisar
4. Verifique se os dados aparecem corretamente

---

## 🔄 Atualizar o Site

Sempre que fizer mudanças, apenas faça:

```bash
git add .
git commit -m "Sua atualização"
git push
```

O deploy é automático em alguns minutos!

---

## 🐛 Problemas?

- **App não inicia:** Veja os logs no painel do Railway/Render
- **Erro de módulo:** Verifique se `requirements.txt` está completo
- **Timeout (Render):** Render pode ter timeout se não houver tráfego por 30 segundos

