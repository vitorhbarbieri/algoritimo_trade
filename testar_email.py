#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para testar configuração de email."""

import json
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from src.email_notifier import EmailNotifier
except ImportError:
    from email_notifier import EmailNotifier

def testar_email():
    """Testa configuração de email."""
    print("=" * 50)
    print("🧪 Teste de Configuração de Email")
    print("=" * 50)
    print()
    
    # Carregar config
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo config.json não encontrado!")
        return False
    
    # Verificar configurações
    print("📋 Verificando configurações...")
    print(f"   Email habilitado: {config.get('email_notifications_enabled', False)}")
    print(f"   Destinatário: {config.get('email_destinatario', 'NÃO CONFIGURADO')}")
    print(f"   Remetente: {config.get('email_remetente', 'NÃO CONFIGURADO')}")
    print(f"   SMTP Server: {config.get('email_smtp_server', 'NÃO CONFIGURADO')}")
    print(f"   SMTP Port: {config.get('email_smtp_port', 'NÃO CONFIGURADO')}")
    print()
    
    if not config.get('email_notifications_enabled', False):
        print("⚠️  Notificações por email estão desabilitadas!")
        print("   Configure 'email_notifications_enabled': true no config.json")
        return False
    
    if not config.get('email_remetente') or not config.get('email_senha'):
        print("❌ Email remetente ou senha não configurados!")
        print("   Configure 'email_remetente' e 'email_senha' no config.json")
        print()
        print("💡 Para Gmail:")
        print("   1. Acesse: https://myaccount.google.com/apppasswords")
        print("   2. Gere uma senha de app")
        print("   3. Use essa senha no config.json")
        return False
    
    # Criar notificador
    print("📧 Criando EmailNotifier...")
    notifier = EmailNotifier(config)
    
    # Testar envio
    print("📤 Enviando email de teste...")
    print()
    
    # Criar oportunidade de teste
    oportunidade_teste = {
        'type': 'vol_arb',
        'ticker': 'AAPL',
        'strike': 150,
        'expiry': '2024-02-15',
        'option_type': 'C',
        'mispricing': 0.25,
        'iv_spread': 0.10,
        'market_price': 3.50,
        'theoretical_price': 2.80,
        'market_iv': 0.35,
        'hist_vol': 0.25,
        'opportunity_score': 0.85
    }
    
    sucesso = notifier.notify_opportunity_found(oportunidade_teste)
    
    if sucesso:
        print("✅ Email de teste enviado com sucesso!")
        print(f"   Verifique a caixa de entrada de {config.get('email_destinatario')}")
        return True
    else:
        print("❌ Erro ao enviar email de teste!")
        print("   Verifique:")
        print("   - Credenciais estão corretas")
        print("   - Senha de app está configurada (Gmail)")
        print("   - Firewall não está bloqueando")
        print("   - SMTP server e porta estão corretos")
        return False

if __name__ == '__main__':
    sucesso = testar_email()
    sys.exit(0 if sucesso else 1)

