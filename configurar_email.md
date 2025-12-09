# 📧 Configurar Notificações por Email

O sistema agora envia emails automaticamente quando encontra oportunidades, assimetrias ou erros.

## ⚙️ Configuração

### 1. Editar config.json

Abra `config.json` e configure:

```json
{
  "email_notifications_enabled": true,
  "email_destinatario": "vitorh.barbieri@gmail.com",
  "email_remetente": "seu_email@gmail.com",
  "email_senha": "sua_senha_app",
  "email_smtp_server": "smtp.gmail.com",
  "email_smtp_port": 587,
  "email_cooldown_seconds": 300
}
```

### 2. Configurar Gmail

Para usar Gmail, você precisa criar uma **Senha de App**:

1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione "Email" e "Outro (nome personalizado)"
3. Digite "Trading System"
4. Clique em "Gerar"
5. Copie a senha gerada (16 caracteres)
6. Use essa senha no campo `email_senha` do config.json

**⚠️ IMPORTANTE:** Não use sua senha normal do Gmail! Use apenas senhas de app.

### 3. Outros Provedores

**Outlook/Hotmail:**
```json
{
  "email_smtp_server": "smtp-mail.outlook.com",
  "email_smtp_port": 587
}
```

**Yahoo:**
```json
{
  "email_smtp_server": "smtp.mail.yahoo.com",
  "email_smtp_port": 587
}
```

## 📨 Tipos de Notificações

### 1. Oportunidades Encontradas

O sistema envia email quando encontra:
- **Volatility Arbitrage**: Opções com IV diferente da histórica
- **Pairs Trading**: Spread entre ativos cointegrados
- **Spread Arbitrage**: Spreads bid-ask anormais
- **Momentum**: Tendências fortes identificadas
- **Mean Reversion**: Desvios extremos de preço

**Critério:** Apenas oportunidades com `opportunity_score > 0.5` geram email.

### 2. Erros do Sistema

Emails são enviados quando:
- Erro ao escanear mercado
- Erro ao buscar dados
- Erro ao processar propostas
- Outros erros críticos

### 3. Eventos de Risco

Emails são enviados quando:
- Exposição máxima excedida
- Limites de gregos excedidos
- Kill switch ativado

### 4. Kill Switch

Email especial quando kill switch é ativado:
- Perda > 15% do NAV inicial
- Todas as operações são interrompidas
- Requer ação manual

## ⏱️ Cooldown (Evitar Spam)

O sistema tem um cooldown de **5 minutos** (300 segundos) entre emails do mesmo tipo para evitar spam.

Você pode ajustar em `config.json`:
```json
{
  "email_cooldown_seconds": 300
}
```

## 🧪 Testar Configuração

Execute o script de teste:

```powershell
python testar_email.py
```

Isso enviará um email de teste para verificar se a configuração está correta.

## 📊 Exemplo de Emails

### Oportunidade Encontrada

```
Assunto: 🎯 Oportunidade Encontrada: VOL_ARB - AAPL

Nova Oportunidade de Trading

Tipo: Vol Arb
Ativo: AAPL
Score: 0.85
Data/Hora: 15/01/2024 14:30:00

Detalhes:
{
  "type": "vol_arb",
  "ticker": "AAPL",
  "strike": 150,
  "mispricing": 0.28,
  "iv_spread": 0.10
}
```

### Erro

```
Assunto: ⚠️ Erro no Sistema: Erro no Scan de Mercado

Erro no Sistema

Tipo: Erro no Scan de Mercado
Mensagem: Connection timeout
Data/Hora: 15/01/2024 14:35:00
```

### Kill Switch

```
Assunto: 🛑 KILL SWITCH ATIVADO!

KILL SWITCH ATIVADO

ATENÇÃO: Sistema Parado por Segurança
Perda: -18.50%
Motivo: Perda de NAV: -18.50%
```

## 🔧 Desabilitar Notificações

Para desabilitar temporariamente:

```json
{
  "email_notifications_enabled": false
}
```

Ou comente as linhas de notificação no código.

## 📝 Próximos Passos

1. Configure `config.json` com suas credenciais
2. Teste com `python testar_email.py`
3. Inicie o monitoramento
4. Receba emails automaticamente!

---

**Fim do Guia**

