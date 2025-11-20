# 🤖 Instalar BMAD Method - Squad de Agentes

O **BMAD (Build, Measure, Analyze, Deploy)** é uma metodologia que cria uma equipe virtual de desenvolvimento com múltiplos agentes de IA trabalhando juntos.

## 📋 Pré-requisitos

### 1. Instalar Node.js

O BMAD requer Node.js. Siga estes passos:

1. **Baixar Node.js:**
   - Acesse: https://nodejs.org/
   - Baixe a versão LTS (recomendada)
   - Execute o instalador
   - Marque todas as opções durante a instalação

2. **Verificar instalação:**
   ```powershell
   node --version
   npm --version
   ```

   Deve mostrar as versões instaladas.

## 🚀 Instalação do BMAD

### Opção 1: Instalação Automática (Recomendada)

Após instalar Node.js, execute:

```powershell
cd c:\Projetos\algoritimo_trade
npx bmad-method install
```

O instalador irá:
- ✅ Fazer perguntas sobre configuração
- ✅ Escolher tipo de instalação
- ✅ Configurar documentação
- ✅ Selecionar IDEs (incluindo Cursor)
- ✅ Criar estrutura de agentes

### Opção 2: Instalação Manual (Modo Rápido)

Se preferir instalação manual:

1. **Baixar arquivos do BMAD:**
   - Acesse: https://github.com/bmad-method/bmad-method
   - Baixe ou clone o repositório
   - Copie os arquivos de configuração para seu projeto

2. **Configurar manualmente:**
   - Crie pasta `.bmad/` no projeto
   - Adicione arquivos de configuração
   - Configure agentes conforme documentação

## 🔧 Configuração no Cursor

### 1. Habilitar Agentes em Segundo Plano

No Cursor:

1. **Abrir configurações:**
   - Pressione `Ctrl+,` (vírgula)
   - Ou: File → Preferences → Settings

2. **Buscar "Background Agent":**
   - Digite "background agent" na busca
   - Habilite a opção

3. **Acessar agentes:**
   - Pressione `Ctrl+E` para modo de agente em segundo plano
   - Ou use a barra lateral de agentes

### 2. Conectar ao GitHub (Opcional)

Para agentes acessarem seu repositório:

1. **No Cursor:**
   - Settings → Accounts → GitHub
   - Conecte sua conta GitHub
   - Conceda permissões de leitura/escrita

2. **No GitHub:**
   - Settings → Developer settings → Personal access tokens
   - Crie token com permissão `repo`
   - Use o token no Cursor se solicitado

## 📁 Estrutura do BMAD

Após instalação, você terá:

```
algoritimo_trade/
├── .bmad/              # Configurações do BMAD
│   ├── agents/         # Configuração de agentes
│   ├── workflows/      # Fluxos de trabalho
│   └── config.json     # Configuração principal
├── docs/               # Documentação gerada
└── ...
```

## 🎯 Usando a Squad de Agentes

### Iniciar Agentes

```powershell
# Via Cursor
Ctrl+E  # Modo de agente em segundo plano
```

### Tipos de Agentes Disponíveis

O BMAD geralmente inclui:

1. **Builder** - Constrói e compila código
2. **Tester** - Executa testes
3. **Analyzer** - Analisa código e performance
4. **Deployer** - Faz deploy
5. **Documenter** - Gera documentação
6. **Reviewer** - Revisa código

### Comandos Úteis

```powershell
# Listar agentes ativos
npx bmad-method list

# Iniciar agente específico
npx bmad-method start <agent-name>

# Parar agente
npx bmad-method stop <agent-name>

# Ver status
npx bmad-method status
```

## 🔗 Links Úteis

- **BMAD Method GitHub:** https://github.com/bmad-method/bmad-method
- **Documentação BMAD:** https://www.dio.me/articles/bmad-method
- **Cursor Background Agents:** https://docs.cursor.com/pt-BR/background-agent

## ⚠️ Troubleshooting

### Erro: "node não é reconhecido"
- ✅ Instale Node.js: https://nodejs.org/
- ✅ Reinicie o terminal após instalar
- ✅ Verifique se está no PATH

### Erro: "npx não encontrado"
- ✅ Node.js não está instalado corretamente
- ✅ Reinstale Node.js
- ✅ Verifique: `npm --version`

### Agentes não aparecem no Cursor
- ✅ Verifique se Background Agents está habilitado
- ✅ Reinicie o Cursor
- ✅ Verifique permissões do GitHub (se conectado)

## ✅ Checklist

- [ ] Node.js instalado (`node --version`)
- [ ] npm funcionando (`npm --version`)
- [ ] BMAD instalado (`npx bmad-method install`)
- [ ] Cursor configurado (Background Agents habilitado)
- [ ] GitHub conectado (opcional)
- [ ] Agentes funcionando (`Ctrl+E`)

## 🎉 Pronto!

Agora você tem uma squad completa de agentes trabalhando no seu projeto!

---

**Última atualização:** Janeiro 2025


