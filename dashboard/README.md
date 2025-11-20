# 📊 Dashboard de Controle

Dashboard web para visualizar e controlar o sistema de trading algorítmico.

## 🚀 Como Acessar

### Opção 1: Via script batch (Windows)
```bash
cd dashboard
start_dashboard.bat
```

### Opção 2: Via Python
```bash
cd dashboard
python app.py
```

### Opção 3: Via linha de comando
```bash
cd C:\Projetos\algoritimo_trade\dashboard
python app.py
```

## 🌐 URL de Acesso

Após iniciar, acesse no navegador:

```
http://localhost:5000
```

ou

```
http://127.0.0.1:5000
```

## 📋 Funcionalidades do Dashboard

- ✅ **Status do Sistema**: Capital atual, retorno, posições abertas
- ✅ **Análise de Tickers**: Selecionar ticker e ver sinais em tempo real
- ✅ **Indicadores Técnicos**: RSI, MACD, Sentimento
- ✅ **Histórico de Operações**: Últimas 10 operações executadas
- ✅ **Atualização Automática**: Status atualiza a cada 5 segundos

## 🔧 Estrutura

```
dashboard/
├── app.py              # Servidor Flask
├── templates/
│   └── index.html      # Interface web
└── start_dashboard.bat # Script de inicialização
```

## 📝 Notas

- O dashboard roda na porta **5000** por padrão
- Certifique-se de ter instalado todas as dependências: `pip install -r ../requirements.txt`
- O dashboard usa o executor mock (não executa trades reais)






