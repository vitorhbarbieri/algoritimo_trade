#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para atualizar monitoring_service.py com notificações por email."""

import re

# Ler arquivo
with open('src/monitoring_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar email_notifier após scan_all_opportunities
pattern = r'(opportunities = self\.market_monitor\.scan_all_opportunities\(market_data\))\s+(# Gerar propostas)'
replacement = r'''\1
                
                # Enviar email se encontrar oportunidades
                if opportunities:
                    self.daily_summary['opportunities_found'] += len(opportunities)
                    
                    # Enviar email para oportunidades importantes (score > threshold)
                    important_opportunities = [opp for opp in opportunities if opp.get('opportunity_score', 0) > 0.5]
                    
                    if len(important_opportunities) == 1:
                        # Uma oportunidade importante
                        self.email_notifier.notify_opportunity_found(important_opportunities[0])
                    elif len(important_opportunities) > 1:
                        # Múltiplas oportunidades
                        self.email_notifier.notify_multiple_opportunities(important_opportunities)

\2'''
content = re.sub(pattern, replacement, content)

# Adicionar contador de propostas
pattern = r'(proposals = self\.trader_agent\.generate_proposals\([^)]+\))\s+(if self\.crypto_api:)'
replacement = r'''\1
                    self.daily_summary['proposals_generated'] += len(proposals)

\2'''
content = re.sub(pattern, replacement, content)

# Adicionar notificação de erro
pattern = r'(except Exception as e:\s+logger\.error\(f"Erro ao escanear mercado: \{e\}"\))'
replacement = r'''\1
            self.daily_summary['errors'] += 1
            # Enviar email de erro
            self.email_notifier.notify_error(
                'Erro no Scan de Mercado',
                str(e),
                {'timestamp': datetime.now().isoformat()}
            )'''
content = re.sub(pattern, replacement, content)

# Salvar
with open('src/monitoring_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ monitoring_service.py atualizado com notificações por email!")

