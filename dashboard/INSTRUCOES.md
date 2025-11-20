# 🔧 Instruções para Resolver Problemas do Dashboard

## ⚠️ Se o Dashboard Está Dando Erro e Saindo do Ar

### Opção 1: Usar Versão Simplificada (Recomendado)

```bash
cd C:\Projetos\algoritimo_trade\dashboard
python app_simples.py
```

Esta versão é mais robusta e não depende de todos os módulos.

### Opção 2: Verificar Erros Específicos

1. **Testar imports:**
```bash
python test_dashboard.py
```

2. **Verificar se Flask está instalado:**
```bash
pip install flask
```

3. **Verificar se todas as dependências estão instaladas:**
```bash
cd C:\Projetos\algoritimo_trade
pip install -r requirements.txt
```

### Opção 3: Usar Versão Completa com Tratamento de Erros

A versão `app.py` foi atualizada com tratamento de erros melhor. Tente:

```bash
cd C:\Projetos\algoritimo_trade\dashboard
python app.py
```

## 📊 URLs de Acesso

- **Dashboard Simplificado**: http://localhost:5000
- **Dashboard Completo**: http://localhost:5000

## 🔍 Verificar o que está acontecendo

Se o servidor está caindo, verifique:

1. **Porta 5000 já está em uso?**
   - Feche outros programas usando a porta 5000
   - Ou mude a porta no código: `app.run(port=5001)`

2. **Erros de importação?**
   - Execute: `python test_dashboard.py`
   - Verifique se todos os módulos estão no lugar certo

3. **Erros de permissão?**
   - Execute como administrador se necessário

## 💡 Solução Rápida

Use a versão simplificada que é mais estável:

```bash
cd C:\Projetos\algoritimo_trade\dashboard
python app_simples.py
```

Depois acesse: **http://localhost:5000**






