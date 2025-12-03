# 📘 Guia do Usuário — Casa Git Compact

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     ██████╗ █████╗ ███████╗ █████╗                                        ║
║    ██╔════╝██╔══██╗██╔════╝██╔══██╗                                       ║
║    ██║     ███████║███████╗███████║                                       ║
║    ██║     ██╔══██║╚════██║██╔══██║                                       ║
║    ╚██████╗██║  ██║███████║██║  ██║                                       ║
║     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                       ║
║                                                                           ║
║              🗜️  GIT COMPACT v1.0  🗜️                                    ║
║                                                                           ║
║         Compacte seus repositórios Git de forma segura!                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 📑 Índice

1. [O que é o Casa Git Compact?](#-1-o-que-é-o-casa-git-compact)
2. [Por que usar?](#-2-por-que-usar)
3. [Pré-requisitos](#-3-pré-requisitos)
4. [Instalação passo a passo](#-4-instalação-passo-a-passo)
5. [Conceitos básicos de Git](#-5-conceitos-básicos-de-git-para-entender-o-script)
6. [Como executar o script](#-6-como-executar-o-script)
7. [Todos os parâmetros explicados](#-7-todos-os-parâmetros-explicados)
8. [Exemplos práticos](#-8-exemplos-práticos)
9. [Entendendo a saída do script](#-9-entendendo-a-saída-do-script)
10. [Solução de problemas](#-10-solução-de-problemas)
11. [Perguntas frequentes (FAQ)](#-11-perguntas-frequentes-faq)

---

## 🎯 1. O que é o Casa Git Compact?

O **Casa Git Compact** é uma ferramenta que **compacta automaticamente** todos os seus repositórios Git, economizando espaço em disco.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   📁 Antes                          📁 Depois                  │
│   ══════                            ═══════                     │
│                                                                 │
│   projeto-web/                      projeto-web/                │
│   └── .git/ (150 MB) ───────────►   └── .git/ (45 MB)           │
│                                                                 │
│   app-mobile/                       app-mobile/                 │
│   └── .git/ (200 MB) ───────────►   └── .git/ (60 MB)           │
│                                                                 │
│   ════════════════════════════════════════════════════════      │
│   💾 Economia: ~70% do espaço!                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ✨ O que o Casa Git Compact faz:

| Etapa | Descrição |
|-------|-----------|
| 🔍 **Busca** | Encontra TODOS os repositórios Git em uma pasta (e subpastas) |
| 💾 **Backup** | Cria uma cópia de segurança antes de qualquer alteração |
| 📝 **Auto-commit** | Salva automaticamente alterações pendentes |
| 🗜️ **Compacta** | Aplica compressão máxima nos arquivos do Git |
| ✅ **Valida** | Verifica se nada foi perdido ou corrompido |

---

## 💡 2. Por que usar?

### 🤔 Problema comum de estudantes de TI:

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  "Meu HD está cheio e eu nem sei por quê!"                     ║
║                                                                ║
║  📁 Meus Projetos                                              ║
║  ├── 📁 projeto-poo (pasta: 50 MB, .git: 300 MB) 😱           ║
║  ├── 📁 trabalho-web (pasta: 20 MB, .git: 150 MB) 😱          ║
║  ├── 📁 app-mobile (pasta: 80 MB, .git: 500 MB) 😱            ║
║  └── ... mais 20 projetos                                      ║
║                                                                ║
║  Total: 5 GB só em pastas .git! 💀                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### ✅ Solução:

Rode o **Casa Git Compact** UMA VEZ e economize espaço em TODOS os projetos!

---

## 📋 3. Pré-requisitos

Antes de usar o Casa Git Compact, você precisa ter instalado:

### 3.1 🐍 Python 3.12 ou superior

```
┌─────────────────────────────────────────────────────────────────┐
│  Como verificar se você tem Python instalado:                   │
│                                                                 │
│  1. Abra o PowerShell (ou Terminal)                             │
│  2. Digite:                                                     │
│                                                                 │
│     python --version                                            │
│                                                                 │
│  3. Você deve ver algo como:                                    │
│                                                                 │
│     Python 3.12.0   ✅ OK!                                      │
│     Python 3.11.5   ❌ Versão antiga, atualize!                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**🔗 Não tem Python?** Baixe em: https://www.python.org/downloads/

> ⚠️ **IMPORTANTE:** Durante a instalação, marque a opção:
> ☑️ "Add Python to PATH"

---

### 3.2 🔧 Git

```
┌─────────────────────────────────────────────────────────────────┐
│  Como verificar se você tem Git instalado:                      │
│                                                                 │
│  1. Abra o PowerShell (ou Terminal)                             │
│  2. Digite:                                                     │
│                                                                 │
│     git --version                                               │
│                                                                 │
│  3. Você deve ver algo como:                                    │
│                                                                 │
│     git version 2.42.0   ✅ OK!                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**🔗 Não tem Git?** Baixe em: https://git-scm.com/downloads

---

### 3.3 💻 PowerShell (Windows)

Já vem instalado no Windows! Para abrir:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Método 1: Tecla Windows + X → "Windows PowerShell"             │
│                                                                 │
│  Método 2: Tecla Windows → Digite "PowerShell" → Enter          │
│                                                                 │
│  Método 3: Na pasta, Shift + Clique Direito →                   │
│            "Abrir janela do PowerShell aqui"                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📥 4. Instalação passo a passo

### Passo 1: Criar uma pasta para o Casa Git Compact

Escolha um local no seu computador. Sugestão:

```
D:\Scripts\casa-git-compact\
```

Você pode criar pelo Windows Explorer ou pelo PowerShell:

```powershell
# Criar a pasta
New-Item -Path "D:\Scripts\casa-git-compact" -ItemType Directory -Force

# Entrar na pasta
cd D:\Scripts\casa-git-compact
```

---

### Passo 2: Criar os arquivos

Você precisa criar **2 arquivos** na pasta:

```
D:\Scripts\casa-git-compact\
├── 📄 casa_git_compact.py      ← Script Python (o cérebro)
└── 📄 Casa-Git-Compact.ps1     ← Script PowerShell (o executor)
```

#### 📄 Criando o arquivo `casa_git_compact.py`:

1. Abra o **Bloco de Notas** (ou VS Code)
2. Cole o código Python completo (fornecido anteriormente)
3. Salve como `casa_git_compact.py`
   - **Local:** `D:\Scripts\casa-git-compact\`
   - **Tipo:** "Todos os arquivos (*.*)"
   - **Codificação:** UTF-8

#### 📄 Criando o arquivo `Casa-Git-Compact.ps1`:

1. Abra o **Bloco de Notas** (ou VS Code)
2. Cole o código PowerShell completo (fornecido anteriormente)
3. Salve como `Casa-Git-Compact.ps1`
   - **Local:** `D:\Scripts\casa-git-compact\`
   - **Tipo:** "Todos os arquivos (*.*)"

---

### Passo 3: Verificar a instalação

```powershell
# Vá até a pasta
cd D:\Scripts\casa-git-compact

# Liste os arquivos
Get-ChildItem

# Você deve ver:
#
#     Mode                 LastWriteTime         Length Name
#     ----                 -------------         ------ ----
#     -a----        03/12/2024     10:00          15000 casa_git_compact.py
#     -a----        03/12/2024     10:00           5000 Casa-Git-Compact.ps1
```

✅ Se você vê os dois arquivos, a instalação está completa!

---

## 📚 5. Conceitos básicos de Git (para entender o script)

> 💡 Se você já sabe o que é Git, pode pular esta seção!

### 🤔 O que é Git?

Git é um **sistema de controle de versão** — ele salva o histórico de todas as alterações dos seus arquivos.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Imagine o Git como uma "máquina do tempo" para seu código:     │
│                                                                 │
│  📅 Segunda:  Versão 1 do projeto ─────┐                        │
│  📅 Terça:    Versão 2 (novas funções) │                        │
│  📅 Quarta:   Versão 3 (bug corrigido) ├──► Git guarda TUDO!    │
│  📅 Quinta:   Versão 4 (novo layout)   │                        │
│  📅 Sexta:    Versão 5 (versão final)  ─┘                       │
│                                                                 │
│  Com Git você pode voltar para qualquer versão anterior!        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📁 O que é a pasta `.git`?

Todo projeto que usa Git tem uma pasta oculta chamada `.git`:

```
meu-projeto/
├── 📁 .git/          ← Aqui o Git guarda TODO o histórico
│   ├── objects/      ← Todas as versões dos arquivos
│   ├── refs/         ← Branches e tags
│   └── ...
├── 📄 index.html
├── 📄 style.css
└── 📄 script.js
```

> ⚠️ **A pasta `.git` pode ficar MUITO grande!** Por isso usamos o Casa Git Compact para compactá-la.

### 📝 O que é um "commit"?

Um **commit** é como um "checkpoint" no seu projeto:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  git add .                    ← Prepara as alterações           │
│  git commit -m "Mensagem"     ← Salva o checkpoint              │
│                                                                 │
│  Exemplo:                                                       │
│  git commit -m "Adicionei o formulário de login"                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 O que são "alterações não commitadas"?

São arquivos que você **modificou** mas **ainda não salvou** no histórico do Git:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Você editou o arquivo "index.html"                             │
│                    ↓                                            │
│  O Git detecta: "Ei, tem coisa nova aqui!"                      │
│                    ↓                                            │
│  Mas você ainda não fez "commit"                                │
│                    ↓                                            │
│  = Alteração NÃO commitada (pendente)                           │
│                                                                 │
│  ════════════════════════════════════════════════════════       │
│                                                                 │
│  ✨ O Casa Git Compact faz o commit AUTOMATICAMENTE para você!  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 6. Como executar o script

### 6.1 Abrindo o PowerShell

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. Pressione a tecla Windows (⊞)                               │
│  2. Digite: powershell                                          │
│  3. Clique em "Windows PowerShell"                              │
│                                                                 │
│  Uma janela azul vai abrir:                                     │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Windows PowerShell                                     │     │
│  │ Copyright (C) Microsoft Corporation.                   │     │
│  │                                                        │     │
│  │ PS C:\Users\SeuNome> _                                 │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.2 Navegando até a pasta do Casa Git Compact

```powershell
# Use o comando "cd" (change directory) para navegar
cd D:\Scripts\casa-git-compact
```

---

### 6.3 Executando o script (forma básica)

```powershell
.\Casa-Git-Compact.ps1 -Path "CAMINHO_DA_SUA_PASTA_DE_PROJETOS"
```

#### 🎯 Exemplo real:

Se seus projetos estão em `C:\Users\Maria\Projetos`:

```powershell
.\Casa-Git-Compact.ps1 -Path "C:\Users\Maria\Projetos"
```

---

### 6.4 Primeiro erro comum: Política de execução

Se aparecer este erro:

```
.\Casa-Git-Compact.ps1 : O arquivo não pode ser carregado porque a 
execução de scripts foi desabilitada neste sistema.
```

**Solução:** Execute este comando UMA VEZ (como administrador):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois digite `S` (Sim) para confirmar.

---

## 📖 7. Todos os parâmetros explicados

O Casa Git Compact aceita vários parâmetros para personalizar o comportamento:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  .\Casa-Git-Compact.ps1                                         │
│      -Path "..."           ← Onde buscar repositórios           │
│      -BackupPath "..."     ← Onde salvar backups                │
│      -KeepBackup           ← Manter backups após sucesso        │
│      -DryRun               ← Simular sem fazer nada             │
│      -SkipRemoteCheck      ← Ignorar verificação de remote      │
│      -NoAutoCommit         ← Não fazer commit automático        │
│      -Exclude @(...)       ← Pastas para ignorar                │
│      -LogFile "..."        ← Salvar log em arquivo              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 📁 `-Path` (OBRIGATÓRIO)

**O que faz:** Define a pasta onde o Casa Git Compact vai buscar repositórios Git.

**Tipo:** Caminho de pasta

```powershell
# Exemplos:
-Path "C:\Users\Joao\Projetos"
-Path "D:\Faculdade\Codigo"
-Path "."                        # Pasta atual
```

---

### 💾 `-BackupPath` (opcional)

**O que faz:** Define onde os backups serão salvos.

**Padrão:** Se não informado, cria uma pasta `_casa_git_compact_backups` ao lado de cada repositório.

```powershell
# Exemplos:
-BackupPath "D:\MeusBackups"
-BackupPath "C:\Backup\Git"
```

**Ilustração:**

```
Sem -BackupPath:                      Com -BackupPath "D:\Backups":
                                    
C:\Projetos\                          C:\Projetos\
├── projeto-a\                        ├── projeto-a\
├── projeto-b\                        └── projeto-b\
└── _casa_git_compact_backups\         
    ├── projeto-a_2024...bundle       D:\Backups\
    └── projeto-b_2024...bundle       ├── projeto-a_2024...bundle
                                      └── projeto-b_2024...bundle
```

---

### 🔒 `-KeepBackup` (opcional)

**O que faz:** Mantém os arquivos de backup mesmo depois que a compactação termina com sucesso.

**Padrão:** Sem este parâmetro, os backups são deletados após sucesso.

```powershell
# Usar quando quiser guardar os backups por segurança
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -KeepBackup
```

**Quando usar:**
- ✅ Primeira vez que roda o script (por precaução)
- ✅ Projetos muito importantes
- ❌ Quando tem pouco espaço em disco

---

### 🧪 `-DryRun` (opcional)

**O que faz:** **SIMULA** a execução sem fazer nenhuma alteração real.

**Padrão:** Desabilitado (executa de verdade).

```powershell
# Testar o que vai acontecer, sem risco:
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -DryRun
```

> 💡 **DICA:** Sempre rode com `-DryRun` primeiro para ver quantos repositórios serão afetados!

**Exemplo de saída com DryRun:**

```
[1/5] Processando: C:\Projetos\app-web
[>>] app-web: Auto-commit realizado
[OK] app-web: 150.0 MB -> 150.0 MB (economia: 0.0 B) [DRY-RUN]
```

---

### 🌐 `-SkipRemoteCheck` (opcional)

**O que faz:** Permite compactar repositórios que NÃO têm um remote (GitHub/GitLab) configurado.

**Padrão:** Por segurança, o Casa Git Compact ignora repositórios sem remote.

```powershell
# Usar se você tem projetos locais sem GitHub:
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -SkipRemoteCheck
```

**O que é "remote"?**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Remote = Cópia do seu projeto na nuvem (GitHub, GitLab, etc)   │
│                                                                 │
│  Seu PC                              GitHub                     │
│  ┌──────────┐                        ┌──────────┐               │
│  │ projeto  │ ◄───── remote ──────►  │ projeto  │               │
│  └──────────┘        (origin)        └──────────┘               │
│                                                                 │
│  Se você tem remote = seu projeto está "salvo na nuvem"         │
│  Se NÃO tem remote = só existe no seu PC (mais arriscado)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 📝 `-NoAutoCommit` (opcional)

**O que faz:** Desabilita o commit automático de alterações pendentes.

**Padrão:** Auto-commit está HABILITADO.

```powershell
# Se você não quer commits automáticos:
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -NoAutoCommit
```

**Quando usar:**
- ❌ Geralmente não precisa usar
- ✅ Se você quer controlar manualmente seus commits
- ✅ Se está no meio de uma tarefa e não quer misturar alterações

**Mensagem de auto-commit:**

Quando o Casa Git Compact faz um auto-commit, a mensagem é:
```
Auto Commit por CasaGitCompact [2024-12-03 14:30:00]
```

---

### 🚫 `-Exclude` (opcional)

**O que faz:** Ignora pastas que contenham os padrões especificados.

**Tipo:** Lista de textos

```powershell
# Ignorar uma pasta:
-Exclude "backup"

# Ignorar múltiplas pastas:
-Exclude @("node_modules", "temp", "old", "backup")
```

**Exemplos práticos:**

```powershell
# Ignorar pastas de dependências (node_modules pode ter repos Git internos)
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -Exclude @("node_modules", "vendor")

# Ignorar projetos antigos
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -Exclude @("antigo", "old", "2022")
```

---

### 📄 `-LogFile` (opcional)

**O que faz:** Salva toda a saída do script em um arquivo de texto.

**Tipo:** Caminho de arquivo

```powershell
# Salvar log:
-LogFile "C:\Logs\casa_git_compact.log"
-LogFile "resultado.txt"
```

**Útil para:**
- 📊 Ver resultados depois
- 📧 Compartilhar com alguém
- 🔍 Investigar problemas

---

## 💻 8. Exemplos práticos

### 📌 Exemplo 1: Uso mais simples possível

**Cenário:** Você quer compactar todos os seus projetos.

```powershell
cd D:\Scripts\casa-git-compact
.\Casa-Git-Compact.ps1 -Path "C:\Users\SeuNome\Projetos"
```

---

### 📌 Exemplo 2: Testar antes de executar (RECOMENDADO)

**Cenário:** Você quer ver o que vai acontecer sem fazer nenhuma alteração.

```powershell
.\Casa-Git-Compact.ps1 -Path "C:\Users\SeuNome\Projetos" -DryRun
```

**O que você vai ver:**

```
   ██████╗ █████╗ ███████╗ █████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔══██╗
  ██║     ███████║███████╗███████║
  ██║     ██╔══██║╚════██║██╔══██║
  ╚██████╗██║  ██║███████║██║  ██║
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
       GIT COMPACT v1.0

============================================================
CASA GIT COMPACT
============================================================
Pasta raiz: C:\Users\SeuNome\Projetos
Dry-run: Sim        ← Modo simulação!
Manter backups: Nao
Auto-commit: Sim

Buscando repositorios...
Encontrados: 8 repositorios

[1/8] Processando: C:\Users\SeuNome\Projetos\site-portfolio
[>>] site-portfolio: Auto-commit realizado
[OK] site-portfolio: 45.2 MB -> 45.2 MB [DRY-RUN]

... (continua para todos os repositórios)
```

---

### 📌 Exemplo 3: Execução completa com backup

**Cenário:** Primeira vez usando o script, quer manter backups por segurança.

```powershell
.\Casa-Git-Compact.ps1 `
    -Path "C:\Users\SeuNome\Projetos" `
    -BackupPath "D:\Backups\Git" `
    -KeepBackup `
    -LogFile "D:\Backups\Git\log.txt"
```

> 💡 O caractere ` (backtick) permite quebrar o comando em várias linhas!

---

### 📌 Exemplo 4: Ignorar pastas específicas

**Cenário:** Você tem projetos Node.js e quer ignorar `node_modules`.

```powershell
.\Casa-Git-Compact.ps1 `
    -Path "C:\Projetos" `
    -Exclude @("node_modules", "vendor", ".venv")
```

---

### 📌 Exemplo 5: Compactar projetos locais (sem GitHub)

**Cenário:** Você tem projetos que só existem no seu PC.

```powershell
.\Casa-Git-Compact.ps1 `
    -Path "C:\ProjetosLocais" `
    -SkipRemoteCheck `
    -KeepBackup
```

---

### 📌 Exemplo 6: Comando completo com todas as opções

**Cenário:** Configuração paranóica de segurança máxima.

```powershell
.\Casa-Git-Compact.ps1 `
    -Path "D:\TodosMeusProjetos" `
    -BackupPath "E:\Backups\CasaGitCompact" `
    -KeepBackup `
    -Exclude @("node_modules", "temp", "cache", "old") `
    -LogFile "E:\Backups\CasaGitCompact\execucao.log"
```

---

### 📌 Exemplo 7: Criar um atalho para uso frequente

Crie um arquivo `CompactarMeusProjetos.ps1` na sua área de trabalho:

```powershell
# CompactarMeusProjetos.ps1

# Caminho do Casa Git Compact
$ScriptPath = "D:\Scripts\casa-git-compact\Casa-Git-Compact.ps1"

# Executar
& $ScriptPath `
    -Path "C:\Users\SeuNome\Projetos" `
    -Exclude @("node_modules") `
    -LogFile "$HOME\Desktop\ultimo_log.txt"

# Pausar para ver o resultado
Read-Host "Pressione Enter para fechar"
```

Depois é só dar **duplo clique** no arquivo!

---

### 📌 Exemplo 8: Executar diretamente pelo Python

Se preferir executar o Python diretamente (sem o PowerShell wrapper):

```powershell
# Windows
python D:\Scripts\casa-git-compact\casa_git_compact.py -p "C:\Projetos" --dry-run

# Linux/Mac
python3 ~/scripts/casa-git-compact/casa_git_compact.py -p ~/projetos --dry-run
```

---

## 📊 9. Entendendo a saída do script

Quando você executa o Casa Git Compact, ele mostra várias informações. Veja o que cada uma significa:

### 9.1 Banner inicial

```
   ██████╗ █████╗ ███████╗ █████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔══██╗
  ██║     ███████║███████╗███████║
  ██║     ██╔══██║╚════██║██╔══██║
  ╚██████╗██║  ██║███████║██║  ██║
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
       GIT COMPACT v1.0
```

---

### 9.2 Cabeçalho de configuração

```
============================================================
CASA GIT COMPACT
============================================================
Pasta raiz: C:\Users\Maria\Projetos     ← Onde está buscando
Dry-run: Nao                            ← Se é simulação ou não
Manter backups: Sim                     ← Se vai guardar backups
Auto-commit: Sim                        ← Se faz commit automático

Buscando repositorios...
Encontrados: 12 repositorios            ← Quantos achou
```

---

### 9.3 Processamento de cada repositório

```
[3/12] Processando: C:\Users\Maria\Projetos\app-mobile
       ↑                         ↑
       │                         └── Caminho do repositório
       └── Número atual / Total
```

---

### 9.4 Mensagens de resultado

| Ícone | Cor | Significado |
|-------|-----|-------------|
| `[OK]` | 🟢 Verde | Sucesso! Repositório compactado |
| `[>>]` | 🔵 Azul | Auto-commit foi realizado |
| `[!!]` | 🟡 Amarelo | Ignorado (mas sem erro) |
| `[XX]` | 🔴 Vermelho | Falha (erro) |

**Exemplos:**

```
[>>] app-mobile: Auto-commit realizado
[OK] app-mobile: 150.5 MB -> 48.2 MB (economia: 102.3 MB)
      ↑              ↑          ↑              ↑
      │              │          │              └── Quanto economizou
      │              │          └── Tamanho depois
      │              └── Tamanho antes
      └── Nome do repositório
```

```
[!!] projeto-teste: Ignorado - Arquivos .lock encontrados
                              ↑
                              └── Motivo de ter sido ignorado
```

---

### 9.5 Resumo final

```
============================================================
RESUMO FINAL
============================================================
Total de repositorios: 12        ← Quantos foram encontrados
[OK] Compactados: 10             ← Quantos tiveram sucesso
[>>] Auto-commits realizados: 3  ← Quantos precisaram de commit
[!!] Ignorados: 1                ← Quantos foram pulados
[XX] Falhas: 1                   ← Quantos deram erro
[!!] Restaurados: 0              ← Quantos precisaram restaurar backup

Tamanho total antes: 1.2 GB
Tamanho total depois: 380.5 MB
[OK] Economia total: 843.7 MB    ← 🎉 Quanto você economizou!
```

---

## 🔧 10. Solução de problemas

### ❌ Erro: "Python não encontrado"

```
[XX] Python nao encontrado no PATH
```

**Solução:**

1. Baixe Python: https://www.python.org/downloads/
2. **IMPORTANTE:** Marque "Add Python to PATH" durante instalação
3. Reinicie o PowerShell
4. Tente novamente

---

### ❌ Erro: "Python 3.11 encontrado, mas é necessário 3.12+"

**Solução:**

1. Baixe a versão mais recente do Python
2. Desinstale a versão antiga (opcional)
3. Reinicie o PowerShell

---

### ❌ Erro: "Script Python não encontrado"

```
[XX] Script Python nao encontrado: D:\Scripts\casa-git-compact\casa_git_compact.py
```

**Solução:**

Verifique se os dois arquivos estão na mesma pasta:
- `Casa-Git-Compact.ps1`
- `casa_git_compact.py` ← Este está faltando!

---

### ❌ Erro: "Arquivos .lock encontrados"

```
[!!] meu-projeto: Ignorado - Arquivos .lock encontrados
```

**Causa:** Uma operação Git anterior não terminou corretamente.

**Solução:**

1. Vá até a pasta do projeto
2. Entre na pasta `.git`
3. Delete arquivos terminados em `.lock`
4. Rode o Casa Git Compact novamente

```powershell
# Ou faça pelo PowerShell:
Remove-Item "C:\Projetos\meu-projeto\.git\*.lock" -Force
Remove-Item "C:\Projetos\meu-projeto\.git\**\*.lock" -Force
```

---

### ❌ Erro: "Nenhum remote configurado"

```
[!!] projeto-local: Ignorado - Nenhum remote configurado
```

**Causa:** O projeto não está conectado ao GitHub/GitLab.

**Soluções:**

**Opção 1:** Use `-SkipRemoteCheck` se você sabe o que está fazendo:
```powershell
.\Casa-Git-Compact.ps1 -Path "C:\Projetos" -SkipRemoteCheck
```

**Opção 2:** Conecte o projeto ao GitHub primeiro:
```powershell
cd C:\Projetos\projeto-local
git remote add origin https://github.com/seu-usuario/projeto-local.git
git push -u origin main
```

---

### ❌ Erro: "A execução de scripts foi desabilitada"

**Solução:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Digite `S` para confirmar.

---

### ❌ Erro: "Falha no fsck"

```
[!!] projeto: Ignorado - Falha no fsck: ...
```

**Causa:** O repositório Git está corrompido.

**Solução:**

1. Clone novamente do GitHub (se tiver)
2. Ou tente reparar:
```powershell
cd C:\Projetos\projeto-corrompido
git fsck --full
git gc --prune=now
```

---

### ❌ Erro: "Falha no auto-commit"

```
[XX] projeto: FALHA - Falha no auto-commit: ...
```

**Possíveis causas:**
- Git não está configurado com nome/email
- Problemas de permissão

**Solução:**

Configure o Git globalmente:
```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

## ❓ 11. Perguntas frequentes (FAQ)

### 🤔 "O Casa Git Compact vai deletar meus arquivos?"

**NÃO!** O script NUNCA deleta seus arquivos de código. Ele apenas compacta a pasta `.git` (o histórico).

---

### 🤔 "É seguro usar?"

**SIM!** O Casa Git Compact foi projetado com várias camadas de segurança:

```
┌─────────────────────────────────────────────────────────────────┐
│  🛡️ CAMADAS DE SEGURANÇA                                        │
│                                                                 │
│  1. Faz backup ANTES de qualquer alteração                      │
│  2. Verifica integridade antes e depois                         │
│  3. Conta commits/branches/tags para garantir que nada mudou    │
│  4. Se algo der errado, restaura o backup automaticamente       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🤔 "Quanto espaço vou economizar?"

Depende dos seus projetos, mas geralmente:

| Tipo de projeto | Economia típica |
|-----------------|-----------------|
| Projetos pequenos (< 50 commits) | 30-50% |
| Projetos médios (50-500 commits) | 50-70% |
| Projetos grandes (> 500 commits) | 60-80% |

---

### 🤔 "Com que frequência devo rodar o Casa Git Compact?"

- **Mínimo:** Uma vez por mês
- **Ideal:** Uma vez por semana
- **Após muitos commits:** Sempre que fizer muitos commits de uma vez

---

### 🤔 "Posso usar em projetos de trabalho/empresa?"

**Sim**, mas:
1. Rode com `-DryRun` primeiro
2. Use `-KeepBackup` por precaução
3. Avise sua equipe antes

---

### 🤔 "O que é o arquivo .bundle criado no backup?"

É um arquivo que contém TODO o seu repositório Git em um único arquivo. Você pode restaurar completamente seu projeto a partir dele.

---

### 🤔 "O que significa 'Auto Commit por CasaGitCompact'?"

Quando o Casa Git Compact encontra alterações não salvas (não commitadas), ele automaticamente cria um commit com a mensagem:

```
Auto Commit por CasaGitCompact [2024-12-03 14:30:00]
```

Isso garante que nenhuma alteração seja perdida durante a compactação.

---

### 🤔 "Posso cancelar no meio da execução?"

**Sim!** Pressione `Ctrl + C`. O repositório atual pode ficar em estado inconsistente, mas o Casa Git Compact não terá tocado nos próximos. Use o backup para restaurar se necessário.

---

### 🤔 "O Casa Git Compact funciona no Linux/Mac?"

**Sim!** O script Python (`casa_git_compact.py`) funciona em qualquer sistema operacional. Apenas execute diretamente:

```bash
# Linux/Mac
python3 casa_git_compact.py -p ~/projetos --dry-run
```

O script PowerShell (`Casa-Git-Compact.ps1`) é específico para Windows.

---

## 📁 Referência rápida de arquivos

```
casa-git-compact/
│
├── 📄 casa_git_compact.py       ← Script Python principal
│                                   (funciona em qualquer SO)
│
├── 📄 Casa-Git-Compact.ps1      ← Wrapper PowerShell (Windows)
│                                   (valida requisitos e chama o Python)
│
└── 📄 README.md                 ← Esta documentação
```

---

## 🎉 Conclusão

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  Parabéns! Você aprendeu a usar o Casa Git Compact!           ║
║                                                               ║
║  📋 Resumo do que você pode fazer:                            ║
║                                                               ║
║  ✅ Compactar todos os seus repositórios Git                  ║
║  ✅ Economizar espaço em disco                                ║
║  ✅ Fazer isso de forma segura (com backups automáticos)      ║
║  ✅ Personalizar o comportamento com parâmetros               ║
║                                                               ║
║  🚀 Comando mais usado:                                       ║
║                                                               ║
║  .\Casa-Git-Compact.ps1 -Path "C:\Projetos" -DryRun           ║
║                                                               ║
║  (Sempre teste com -DryRun primeiro!)                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📞 Suporte

**📧 Dúvidas?** Procure seu professor ou monitor!

**🐛 Encontrou um bug?** Documente o erro e reporte!

---

```
   ██████╗ █████╗ ███████╗ █████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔══██╗
  ██║     ███████║███████╗███████║   Made with ❤️ for IT students
  ██║     ██╔══██║╚════██║██╔══██║
  ╚██████╗██║  ██║███████║██║  ██║
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
       GIT COMPACT v1.0
```