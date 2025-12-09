#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para atualizar RiskAgent com notificações por email."""

import re

# Ler arquivo
with open('src/agents.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Adicionar import do EmailNotifier
pattern = r'(from \.utils import StructuredLogger)'
replacement = r'''\1
try:
    from .email_notifier import EmailNotifier
except ImportError:
    from email_notifier import EmailNotifier'''
content = re.sub(pattern, replacement, content)

# Adicionar email_notifier ao __init__ do RiskAgent
pattern = r'(def __init__\(self, portfolio_manager: PortfolioManager, config: Dict, logger: Optional\[StructuredLogger\] = None\):.*?self\.kill_switch_active = False)'
replacement = r'''\1
        self.email_notifier = EmailNotifier(config) if config.get('email_notifications_enabled', True) else None'''
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Adicionar notificação quando kill switch é ativado
pattern = r'(def kill_switch\(self\):\s+"""Ativa kill switch\."""\s+self\.kill_switch_active = True\s+if self\.logger:\s+self\.logger\.log_decision\('kill_switch', \{'active': True\}\)\s*)'
replacement = r'''\1
        # Notificar por email
        if self.email_notifier:
            nav_loss = (self.portfolio.initial_nav - self.portfolio.nav) / self.portfolio.initial_nav if self.portfolio.initial_nav > 0 else 0
            self.email_notifier.notify_kill_switch(
                f'Perda de NAV: {nav_loss:.2%}',
                nav_loss
            )
        '''
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Adicionar notificação para eventos de risco importantes
# Procurar por rejeições importantes
pattern = r'(return \('REJECT', None, f'Exposição máxima excedida: \{current_exposure:.2f\}'\))'
replacement = r'''\1
            # Notificar evento de risco
            if self.email_notifier:
                self.email_notifier.notify_risk_event(
                    'Exposição Máxima Excedida',
                    f'Exposição atual: {current_exposure:.2f}, Limite: {self.portfolio.nav * max_exposure:.2f}',
                    {'exposure': current_exposure, 'limit': self.portfolio.nav * max_exposure}
                )'''
content = re.sub(pattern, replacement, content)

# Salvar
with open('src/agents.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ agents.py atualizado com notificações por email!")

