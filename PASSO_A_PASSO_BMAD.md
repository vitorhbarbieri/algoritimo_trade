# 🚀 Passo a Passo: Instalar BMAD no Cursor

## ⚠️ IMPORTANTE: Node.js Necessário

O BMAD precisa do Node.js. Se não tiver instalado, siga primeiro o **Passo 1**.

---

## 📋 Passo 1: Instalar Node.js (Se Não Tiver)

### Opção A: Download Manual

1. **Acesse:** https://nodejs.org/
2. **Baixe:** Versão LTS (Long Term Support) - recomendada
3. **Execute:** O instalador baixado
4. **Durante instalação:** Marque todas as opções
5. **Reinicie:** O terminal/PowerShell após instalar

### Opção B: Via Chocolatey (Se Tiver)

```powershell
choco install nodejs-lts
```

### Verificar Instalação

Abra um **NOVO** terminal e execute:

```powershell
node --version
npm --version
```

Se mostrar versões, está instalado! ✅

---

## 📋 Passo 2: Instalar BMAD Method

### No Terminal (PowerShell):

```powershell
# Navegar para o projeto
cd c:\Projetos\algoritimo_trade

# Instalar BMAD
npx bmad-method install
```

### Durante a Instalação:

O instalador fará perguntas:

1. **Tipo de instalação:**
   - Escolha: `Professional` (recomendado)
   - Ou: `Quick` (mais simples)

2. **Diretório:**
   - Deixe padrão: `.bmad/`

3. **IDEs:**
   - ✅ Marque: **Cursor**
   - ✅ Marque outras IDEs que usar (VS Code, etc.)

4. **Documentação:**
   - Escolha como organizar docs

5. **Web Bundles:**
   - Escolha se quer incluir

### Após Instalação:

Você verá:
```
✅ BMAD Method instalado com sucesso!
📁 Estrutura criada em: .bmad/
🎯 Agentes configurados
```

---

## 📋 Passo 3: Configurar no Cursor

### 3.1 Habilitar Background Agents

1. **Abrir Cursor**
2. **Pressionar:** `Ctrl+,` (vírgula) - abre Settings
3. **Buscar:** "background agent"
4. **Habilitar:** ✅ "Enable Background Agents"
5. **Salvar:** Fechar settings

### 3.2 Acessar Agentes

**Método 1 - Atalho:**
- Pressione: `Ctrl+E`
- Abre painel de Background Agents

**Método 2 - Barra Lateral:**
- Clique no ícone de agentes na barra lateral
- Ou: View → Background Agents

### 3.3 Conectar GitHub (Opcional mas Recomendado)

Para agentes acessarem seu código:

1. **No Cursor:**
   - Settings → Accounts → GitHub
   - Clique em "Connect GitHub"
   - Autorize o Cursor

2. **Permissões:**
   - ✅ Leitura de repositórios
   - ✅ Escrita em repositórios (se quiser que agentes façam commits)

---

## 📋 Passo 4: Usar a Squad de Agentes

### Iniciar Agente

1. **Pressione:** `Ctrl+E`
2. **Clique:** "New Background Agent"
3. **Escolha:** Tipo de agente ou tarefa
4. **Configure:** Parâmetros se necessário
5. **Iniciar:** O agente começa a trabalhar

### Tipos de Agentes Disponíveis

Após instalar BMAD, você terá acesso a:

- 🔨 **Builder** - Constrói e compila
- 🧪 **Tester** - Executa testes
- 📊 **Analyzer** - Analisa código
- 🚀 **Deployer** - Faz deploy
- 📝 **Documenter** - Gera docs
- 👀 **Reviewer** - Revisa código

### Comandos Úteis

```powershell
# Ver agentes disponíveis
npx bmad-method list

# Status dos agentes
npx bmad-method status

# Ver logs
npx bmad-method logs
```

---

## ✅ Verificação Final

Execute estes comandos para verificar:

```powershell
# 1. Node.js instalado?
node --version
npm --version

# 2. BMAD instalado?
npx bmad-method --version

# 3. Estrutura criada?
dir .bmad

# 4. No Cursor: Ctrl+E funciona?
# Deve abrir painel de Background Agents
```

---

## 🐛 Problemas Comuns

### ❌ "node não é reconhecido"
**Solução:**
- Instale Node.js: https://nodejs.org/
- Reinicie o terminal
- Verifique: `node --version`

### ❌ "npx não encontrado"
**Solução:**
- Node.js não instalado corretamente
- Reinstale Node.js
- Verifique PATH do sistema

### ❌ "Ctrl+E não funciona no Cursor"
**Solução:**
- Verifique se Background Agents está habilitado
- Settings → "background agent" → Habilitar
- Reinicie o Cursor

### ❌ "BMAD não instala"
**Solução:**
- Verifique conexão com internet
- Tente: `npm cache clean --force`
- Tente novamente: `npx bmad-method install`

---

## 📚 Documentação Adicional

- **BMAD GitHub:** https://github.com/bmad-method/bmad-method
- **Cursor Docs:** https://docs.cursor.com/pt-BR/background-agent
- **BMAD Artigo:** https://www.dio.me/articles/bmad-method

---

## 🎉 Pronto!

Agora você tem:
- ✅ Node.js instalado
- ✅ BMAD Method configurado
- ✅ Squad de agentes no Cursor
- ✅ Agentes prontos para trabalhar

**Próximo passo:** Pressione `Ctrl+E` no Cursor e comece a usar os agentes!

---

**Última atualização:** Janeiro 2025


