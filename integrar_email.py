#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para integrar notificações por email nos módulos."""

import re
from pathlib import Path

def atualizar_monitoring_service():
    """Atualiza monitoring_service.py."""
    arquivo = Path('src/monitoring_service.py')
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar email_notifier após data_loader
    pattern = r'(self\.data_loader = DataLoader\(\))'
    replacement = r'''\1
        self.email_notifier = EmailNotifier(config)
        self.daily_summary = {
            'opportunities_found': 0,
            'proposals_generated': 0,
            'proposals_approved': 0,
            'proposals_rejected': 0,
            'errors': 0
        }'''
    content = re.sub(pattern, replacement, content)
    
    # Adicionar notificações após scan_all_opportunities
    pattern = r'(opportunities = self\.market_monitor\.scan_all_opportunities\(market_data\))'
    replacement = r'''\1
                
                # Enviar email se encontrar oportunidades
                if opportunities:
                    self.daily_summary['opportunities_found'] += len(opportunities)
                    important_opportunities = [opp for opp in opportunities if opp.get('opportunity_score', 0) > 0.5]
                    if len(important_opportunities) == 1:
                        self.email_notifier.notify_opportunity_found(important_opportunities[0])
                    elif len(important_opportunities) > 1:
                        self.email_notifier.notify_multiple_opportunities(important_opportunities)'''
    content = re.sub(pattern, replacement, content)
    
    # Adicionar contador de propostas
    pattern = r'(proposals = self\.trader_agent\.generate_proposals\([^)]+\))'
    replacement = r'''\1
                    self.daily_summary['proposals_generated'] += len(proposals)'''
    content = re.sub(pattern, replacement, content)
    
    # Adicionar notificação de erro
    pattern = r'(except Exception as e:\s+logger\.error\(f"Erro ao escanear mercado: \{e\}"\))'
    replacement = r'''\1
            self.daily_summary['errors'] += 1
            self.email_notifier.notify_error('Erro no Scan de Mercado', str(e), {'timestamp': datetime.now().isoformat()})'''
    content = re.sub(pattern, replacement, content)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ monitoring_service.py atualizado")

def atualizar_agents():
    """Atualiza agents.py."""
    arquivo = Path('src/agents.py')
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar import
    pattern = r'(from \.utils import StructuredLogger)'
    replacement = r'''\1
try:
    from .email_notifier import EmailNotifier
except ImportError:
    from email_notifier import EmailNotifier'''
    content = re.sub(pattern, replacement, content)
    
    # Adicionar email_notifier ao RiskAgent
    pattern = r'(self\.kill_switch_active = False)'
    replacement = r'''\1
        self.email_notifier = EmailNotifier(config) if config.get('email_notifications_enabled', True) else None'''
    content = re.sub(pattern, replacement, content)
    
    # Adicionar notificação no kill_switch
    pattern = r'(def kill_switch\(self\):\s+"""Ativa kill switch\."""\s+self\.kill_switch_active = True\s+if self\.logger:\s+self\.logger\.log_decision\('kill_switch', \{'active': True\}\))'
    replacement = r'''def kill_switch(self):
        """Ativa kill switch."""
        self.kill_switch_active = True
        if self.logger:
            self.logger.log_decision('kill_switch', {'active': True})
        if self.email_notifier:
            nav_loss = (self.portfolio.initial_nav - self.portfolio.nav) / self.portfolio.initial_nav if self.portfolio.initial_nav > 0 else 0
            self.email_notifier.notify_kill_switch(f'Perda de NAV: {nav_loss:.2%}', nav_loss)'''
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ agents.py atualizado")

if __name__ == '__main__':
    print("Integrando notificações por email...")
    atualizar_monitoring_service()
    atualizar_agents()
    print("\n✅ Integração completa!")

