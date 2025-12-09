#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para enviar relatório por email.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

def enviar_relatorio_email(destinatario='vitorh.barbieri@gmail.com'):
    """Envia relatório por email."""
    
    # Configurações de email (ajustar conforme necessário)
    remetente = os.getenv('EMAIL_REMETENTE', 'seu_email@gmail.com')
    senha = os.getenv('EMAIL_SENHA', 'sua_senha_app')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f'Relatório Completo - Sistema de Trading - {datetime.now().strftime("%d/%m/%Y %H:%M")}'
    
    # Corpo do email
    corpo = f"""
Olá,

Segue em anexo o relatório completo do Sistema de Trading com Agentes Cooperativos.

O relatório contém:
- Arquitetura completa do sistema
- Descrição detalhada dos 5 modelos de assimetria
- Fluxo de processamento
- Como usar o sistema
- Configurações principais

Data de geração: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

Atenciosamente,
Sistema de Trading Automatizado
"""
    
    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
    
    # Anexar relatório
    arquivo_relatorio = 'RELATORIO_COMPLETO_PROJETO.md'
    if os.path.exists(arquivo_relatorio):
        with open(arquivo_relatorio, 'r', encoding='utf-8') as f:
            anexo = MIMEBase('application', 'octet-stream')
            anexo.set_payload(f.read().encode('utf-8'))
            encoders.encode_base64(anexo)
            anexo.add_header(
                'Content-Disposition',
                f'attachment; filename= {arquivo_relatorio}'
            )
            msg.attach(anexo)
    
    # Enviar email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)
        text = msg.as_string()
        server.sendmail(remetente, destinatario, text)
        server.quit()
        print(f"✅ Relatório enviado com sucesso para {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        print("\n💡 DICA: Configure as variáveis de ambiente:")
        print("   export EMAIL_REMETENTE='seu_email@gmail.com'")
        print("   export EMAIL_SENHA='sua_senha_app'")
        print("\n   Ou edite este script diretamente.")
        return False

if __name__ == '__main__':
    import sys
    destinatario = sys.argv[1] if len(sys.argv) > 1 else 'vitorh.barbieri@gmail.com'
    enviar_relatorio_email(destinatario)

