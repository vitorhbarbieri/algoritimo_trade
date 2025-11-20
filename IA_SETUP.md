# 🤖 Configuração do Módulo de IA para Análise de Carteira

Este módulo permite que uma IA analise sua carteira e gere recomendações estratégicas de movimentos (manter, aumentar, reduzir, vender).

## 📋 Requisitos

O módulo suporta dois provedores de IA:

### 1. OpenAI (Recomendado)
- **Biblioteca**: `openai`
- **Instalação**: `pip install openai`
- **Modelo padrão**: `gpt-4o-mini` (pode ser alterado via variável de ambiente)

### 2. Anthropic Claude
- **Biblioteca**: `anthropic`
- **Instalação**: `pip install anthropic`
- **Modelo padrão**: `claude-3-5-sonnet-20241022`

## 🔑 Configuração

### Para usar OpenAI:

#### 🚀 Método Rápido (Windows PowerShell)

Execute o script de configuração:
```powershell
.\configurar_ia.ps1
```

O script irá:
- Solicitar sua API Key
- Configurar a variável de ambiente permanentemente
- Permitir escolher o modelo

Depois, **feche e reabra o terminal** e execute o app novamente.

---

#### 📝 Método Manual

1. **Obtenha uma API key:**
   - Acesse: https://platform.openai.com/api-keys
   - Faça login ou crie uma conta
   - Clique em "Create new secret key"
   - Copie a chave (ela só aparece uma vez!)

2. **Configure a variável de ambiente:**

   #### Método 1: Temporário (apenas para a sessão atual do terminal)
   
   **Windows PowerShell:**
   ```powershell
   $env:OPENAI_API_KEY="sk-sua-chave-aqui"
   ```
   
   **Windows CMD:**
   ```cmd
   set OPENAI_API_KEY=sk-sua-chave-aqui
   ```
   
   **Linux/Mac:**
   ```bash
   export OPENAI_API_KEY="sk-sua-chave-aqui"
   ```
   
   ⚠️ **Importante:** Este método só funciona enquanto o terminal estiver aberto. Ao fechar, a variável é perdida.
   
   #### Método 2: Permanente no Windows (Recomendado)
   
   **Opção A - Via Interface Gráfica:**
   1. Pressione `Win + R`, digite `sysdm.cpl` e pressione Enter
   2. Vá na aba "Avançado"
   3. Clique em "Variáveis de Ambiente"
   4. Em "Variáveis do usuário", clique em "Novo"
   5. Nome: `OPENAI_API_KEY`
   6. Valor: `sk-sua-chave-aqui`
   7. Clique em "OK" em todas as janelas
   8. **Reinicie o terminal** para aplicar as mudanças
   
   **Opção B - Via PowerShell (como Administrador):**
   ```powershell
   [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-sua-chave-aqui', 'User')
   ```
   Depois, reinicie o terminal.
   
   #### Método 3: Arquivo .env (Mais Seguro)
   
   1. Crie um arquivo `.env` na raiz do projeto:
   ```
   OPENAI_API_KEY=sk-sua-chave-aqui
   OPENAI_MODEL=gpt-4o-mini
   ```
   
   2. Instale o pacote `python-dotenv`:
   ```bash
   pip install python-dotenv
   ```
   
   3. Adicione no início do `app_simples.py`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
   
   ⚠️ **Importante:** Adicione `.env` ao `.gitignore` para não commitar sua chave!

3. **(Opcional) Escolha o modelo:**
   ```bash
   # Windows PowerShell
   $env:OPENAI_MODEL="gpt-4o-mini"  # ou "gpt-4", "gpt-3.5-turbo", etc.
   
   # Linux/Mac
   export OPENAI_MODEL="gpt-4o-mini"
   ```
   
   Modelos disponíveis:
   - `gpt-4o-mini` - Mais barato e rápido (recomendado)
   - `gpt-4` - Mais poderoso, mas mais caro
   - `gpt-3.5-turbo` - Alternativa econômica

### Para usar Claude:

1. Obtenha uma API key em: https://console.anthropic.com/
2. Configure a variável de ambiente:
   ```bash
   $env:ANTHROPIC_API_KEY="sua-chave-aqui"
   ```

3. (Opcional) Escolha o modelo:
   ```bash
   $env:ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"
   ```

## 🎯 Como Usar

1. **Importe suas operações** na Home Page
2. **Clique em "Analisar Carteira"** na seção "🤖 Recomendações de IA"
3. A IA irá:
   - Analisar todas as posições abertas
   - Calcular rentabilidades e PnL
   - Gerar recomendações por ticker
   - Fornecer observações gerais e sugestões estratégicas

## 📊 Formato das Recomendações

A IA retorna:
- **Resumo executivo**: Visão geral da carteira
- **Recomendações por ticker**: 
  - Ação sugerida (MANTER, AUMENTAR, REDUZIR, VENDER)
  - Justificativa detalhada
  - Prioridade (ALTA, MÉDIA, BAIXA)
  - Rentabilidade atual
  - Perspectiva de valorização
- **Observações gerais**: Sobre diversificação, risco, etc.
- **Sugestões estratégicas**: Movimentos gerais recomendados

## 🔄 Fallback

Se nenhuma API de IA estiver configurada, o sistema usa recomendações básicas baseadas apenas em rentabilidade:
- Rentabilidade < -10%: REDUZIR
- Rentabilidade > +20%: MANTER
- Outros: MANTER com monitoramento

## 💡 Dicas

- Configure pelo menos uma API para análises mais profundas
- A OpenAI (gpt-4o-mini) é mais barata e rápida
- O Claude oferece análises mais detalhadas
- As recomendações são baseadas nos dados da carteira atual

## ✅ Verificar se está Configurado

### Windows PowerShell:
```powershell
# Verificar se a variável está configurada
$env:OPENAI_API_KEY

# Ou verificar permanentemente
[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')
```

### Linux/Mac:
```bash
echo $OPENAI_API_KEY
```

### Python (teste rápido):
```python
import os
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ API Key configurada: {api_key[:10]}...")
else:
    print("❌ API Key não encontrada!")
```

## 🔧 Solução de Problemas

### "OPENAI_API_KEY não configurada"
- Verifique se a variável está configurada (use os comandos acima)
- Se usou método temporário, certifique-se de que o terminal ainda está aberto
- Se usou método permanente, **reinicie o terminal** após configurar
- Se usou arquivo `.env`, verifique se:
  - O arquivo está na raiz do projeto
  - Tem o nome exato `.env` (não `.env.txt`)
  - Instalou `python-dotenv`: `pip install python-dotenv`

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### A IA não está sendo chamada
- Verifique os logs do servidor Flask
- Certifique-se de que a API Key é válida
- Teste a chave diretamente na API da OpenAI

