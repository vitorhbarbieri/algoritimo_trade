# 🌐 Configurar Acesso Remoto ao Sistema

Este guia explica como deixar o sistema acessível remotamente para monitoramento à distância.

---

## 📋 Opções Disponíveis

### 1. **ngrok** (Mais Fácil - Recomendado)
- ✅ Gratuito
- ✅ Fácil de configurar
- ✅ URL pública temporária
- ⚠️ URL muda a cada reinício (versão gratuita)

### 2. **Cloudflare Tunnel** (Recomendado para Produção)
- ✅ Gratuito
- ✅ URL permanente
- ✅ Mais seguro
- ⚠️ Requer conta Cloudflare

### 3. **Port Forwarding** (Router)
- ✅ Controle total
- ✅ Sem dependências externas
- ⚠️ Requer configuração de router
- ⚠️ Pode expor segurança

---

## 🚀 OPÇÃO 1: ngrok (Recomendado para Testes)

### Passo 1: Instalar ngrok

**Windows:**
```powershell
# Baixar de https://ngrok.com/download
# Ou via Chocolatey:
choco install ngrok

# Ou via Scoop:
scoop install ngrok
```

**Linux/Mac:**
```bash
# Via Homebrew (Mac)
brew install ngrok

# Ou baixar de https://ngrok.com/download
```

### Passo 2: Criar Conta e Obter Token

1. Acesse https://dashboard.ngrok.com/signup
2. Crie uma conta gratuita
3. Copie seu authtoken
4. Execute:
```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

### Passo 3: Criar Script de Inicialização

Crie o arquivo `iniciar_com_acesso_remoto.bat`:

```batch
@echo off
echo ========================================
echo  Iniciando Sistema com Acesso Remoto
echo ========================================

REM Iniciar API Server em background
start "API Server" cmd /k "python api_server.py"

REM Aguardar API iniciar
timeout /t 5 /nobreak >nul

REM Iniciar Dashboard em background
start "Dashboard" cmd /k "streamlit run dashboard_central.py --server.port 8501"

REM Aguardar Dashboard iniciar
timeout /t 5 /nobreak >nul

REM Iniciar ngrok para API (porta 5000)
start "ngrok API" cmd /k "ngrok http 5000"

REM Iniciar ngrok para Dashboard (porta 8501)
start "ngrok Dashboard" cmd /k "ngrok http 8501"

echo.
echo ========================================
echo  Sistema iniciado!
echo ========================================
echo.
echo Acesse o Dashboard em:
echo   http://localhost:8501
echo.
echo Para acesso remoto, veja as URLs do ngrok:
echo   http://localhost:4040 (API)
echo   http://localhost:4040 (Dashboard)
echo.
pause
```

### Passo 4: Executar

```powershell
.\iniciar_com_acesso_remoto.bat
```

### Passo 5: Obter URLs Públicas

1. Abra http://localhost:4040 no navegador
2. Você verá as URLs públicas do ngrok
3. Exemplo:
   - API: `https://abc123.ngrok.io`
   - Dashboard: `https://def456.ngrok.io`

### Passo 6: Acessar Remotamente

Use as URLs do ngrok de qualquer lugar:
- Dashboard: `https://def456.ngrok.io`
- API: `https://abc123.ngrok.io`

---

## 🔒 OPÇÃO 2: Cloudflare Tunnel (Produção)

### Passo 1: Instalar cloudflared

**Windows:**
```powershell
# Baixar de https://github.com/cloudflare/cloudflared/releases
# Ou via Chocolatey:
choco install cloudflared
```

**Linux/Mac:**
```bash
# Mac
brew install cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

### Passo 2: Fazer Login

```bash
cloudflared tunnel login
```

Isso abrirá o navegador para autenticar com sua conta Cloudflare.

### Passo 3: Criar Tunnel

```bash
cloudflared tunnel create trading-system
```

Anote o Tunnel ID retornado.

### Passo 4: Criar Configuração

Crie arquivo `~/.cloudflared/config.yml`:

```yaml
tunnel: SEU_TUNNEL_ID
credentials-file: C:\Users\SEU_USUARIO\.cloudflared\SEU_TUNNEL_ID.json

ingress:
  - hostname: trading-dashboard.SEU_DOMINIO.com
    service: http://localhost:8501
  - hostname: trading-api.SEU_DOMINIO.com
    service: http://localhost:5000
  - service: http_status:404
```

### Passo 5: Configurar DNS

```bash
cloudflared tunnel route dns trading-system trading-dashboard.SEU_DOMINIO.com
cloudflared tunnel route dns trading-system trading-api.SEU_DOMINIO.com
```

### Passo 6: Executar Tunnel

```bash
cloudflared tunnel run trading-system
```

### Passo 7: Acessar

- Dashboard: `https://trading-dashboard.SEU_DOMINIO.com`
- API: `https://trading-api.SEU_DOMINIO.com`

---

## 🔐 OPÇÃO 3: Port Forwarding (Router)

### Passo 1: Configurar Router

1. Acesse o painel do seu router (geralmente `192.168.1.1`)
2. Vá para "Port Forwarding" ou "Virtual Server"
3. Adicione regras:
   - **Porta Externa**: 8501 → **IP Interno**: IP do seu PC → **Porta Interna**: 8501 (Dashboard)
   - **Porta Externa**: 5000 → **IP Interno**: IP do seu PC → **Porta Interna**: 5000 (API)

### Passo 2: Descobrir IP Público

```powershell
# Windows PowerShell
Invoke-RestMethod -Uri "https://api.ipify.org?format=json"
```

### Passo 3: Acessar Remotamente

- Dashboard: `http://SEU_IP_PUBLICO:8501`
- API: `http://SEU_IP_PUBLICO:5000`

⚠️ **ATENÇÃO**: Isso expõe seu sistema diretamente à internet. Use firewall e autenticação!

---

## 🛡️ Segurança para Acesso Remoto

### 1. Adicionar Autenticação ao Dashboard

Edite `dashboard_central.py` e adicione no início:

```python
import streamlit_authenticator as stauth

# Configurar usuário/senha
credentials = {
    "usernames": {
        "admin": {
            "name": "Administrador",
            "password": stauth.Hasher(['sua_senha_segura']).generate()[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'trading_dashboard',
    'abc123',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()
elif authentication_status:
    # Resto do código do dashboard aqui
    pass
```

### 2. Adicionar CORS e Rate Limiting à API

Edite `api_server.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/backtest/run', methods=['POST'])
@limiter.limit("10 per hour")
def run_backtest():
    # ... código existente
```

### 3. Usar HTTPS

Para produção, configure certificado SSL:
- **Let's Encrypt** (gratuito)
- **Cloudflare** (gratuito com proxy)

---

## 📱 Monitoramento Mobile

### Criar App Mobile Simples

Você pode criar uma página HTML simples para acesso mobile:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Trading Dashboard Mobile</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; padding: 10px; }
        .metric { background: #f0f0f0; padding: 10px; margin: 5px; border-radius: 5px; }
        .status { padding: 5px; border-radius: 3px; }
        .online { background: #4CAF50; color: white; }
        .offline { background: #f44336; color: white; }
    </style>
</head>
<body>
    <h1>📊 Trading Dashboard</h1>
    <div id="status" class="status offline">Carregando...</div>
    <div id="metrics"></div>
    
    <script>
        const API_URL = 'https://SUA_URL_NGROK.io';
        
        async function updateStatus() {
            try {
                const res = await fetch(`${API_URL}/health`);
                const data = await res.json();
                document.getElementById('status').innerHTML = 
                    `✅ Sistema Online - ${new Date().toLocaleTimeString()}`;
                document.getElementById('status').className = 'status online';
            } catch (e) {
                document.getElementById('status').innerHTML = 
                    `❌ Sistema Offline`;
                document.getElementById('status').className = 'status offline';
            }
        }
        
        async function loadMetrics() {
            try {
                const res = await fetch(`${API_URL}/backtest/results`);
                const data = await res.json();
                // Exibir métricas
            } catch (e) {
                console.error(e);
            }
        }
        
        setInterval(updateStatus, 30000); // A cada 30 segundos
        setInterval(loadMetrics, 60000); // A cada 1 minuto
        updateStatus();
        loadMetrics();
    </script>
</body>
</html>
```

---

## 🚨 Troubleshooting

### ngrok não conecta
- Verifique se o token está configurado: `ngrok config check`
- Verifique se as portas estão corretas
- Verifique firewall do Windows

### Cloudflare Tunnel não funciona
- Verifique se está logado: `cloudflared tunnel list`
- Verifique configuração DNS
- Verifique logs: `cloudflared tunnel run --loglevel debug`

### Port Forwarding não funciona
- Verifique se o router permite port forwarding
- Verifique se o IP do PC está correto
- Verifique firewall do Windows e do router

---

## 📞 Próximos Passos

1. Escolha uma opção acima
2. Configure conforme instruções
3. Teste acesso remoto
4. Configure autenticação
5. Configure alertas por email/Telegram

---

**Fim do Guia**

