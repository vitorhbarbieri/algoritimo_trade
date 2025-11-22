# 🔄 Plano de Migração para Multi-Tenant

## 📋 Checklist de Migração

### 1. Preparação
- [ ] Backup do banco atual (`trades.db`)
- [ ] Criar branch de migração
- [ ] Testar em ambiente de desenvolvimento primeiro

### 2. Schema do Banco
- [ ] Criar tabela `users`
- [ ] Adicionar coluna `user_id` em `trades`
- [ ] Adicionar coluna `user_id` em `dividendos`
- [ ] Criar índices para performance
- [ ] Adicionar foreign keys

### 3. Migração de Dados Existentes
- [ ] Criar usuário "default" ou "admin"
- [ ] Migrar dados existentes para user_id=1
- [ ] Validar integridade dos dados

### 4. Código
- [ ] Atualizar `trades_repository.py` com user_id
- [ ] Atualizar `dividendos_collector.py` com user_id
- [ ] Criar sistema de autenticação
- [ ] Adicionar middleware de isolamento
- [ ] Atualizar dashboard com login

### 5. Testes
- [ ] Testar isolamento entre usuários
- [ ] Testar autenticação
- [ ] Testar migração de dados
- [ ] Testar todas as funcionalidades

---

## 🚨 Importante

**Dados Existentes:**
- Os dados atuais serão migrados para um usuário "default"
- Após migração, será necessário criar conta para acessar
- Backup é essencial antes de migrar!

---

**Status:** Planejamento  
**Próximo passo:** Implementar estrutura base

