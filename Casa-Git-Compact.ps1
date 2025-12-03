<#
.SYNOPSIS
    CASA GIT COMPACT - Wrapper PowerShell

.DESCRIPTION
    Valida a instalacao do Python 3.12+ e executa o script de compactacao
    de repositorios Git com os parametros fornecidos.

.PARAMETER Path
    Pasta raiz para buscar repositorios Git.

.PARAMETER BackupPath
    Pasta para armazenar backups (opcional).

.PARAMETER KeepBackup
    Manter backups mesmo apos compactacao bem-sucedida.

.PARAMETER DryRun
    Simular sem executar alteracoes.

.PARAMETER SkipRemoteCheck
    Nao exigir remote configurado.

.PARAMETER NoAutoCommit
    Desabilitar auto-commit de alteracoes pendentes.

.PARAMETER Exclude
    Lista de padroes para excluir da busca.

.PARAMETER LogFile
    Arquivo para salvar o log.

.EXAMPLE
    .\Casa-Git-Compact.ps1 -Path "C:\MeusProjetos"

.EXAMPLE
    .\Casa-Git-Compact.ps1 -Path "C:\MeusProjetos" -DryRun -KeepBackup

.EXAMPLE
    .\Casa-Git-Compact.ps1 -Path "D:\Repos" -Exclude "temp", "backup" -LogFile "resultado.log"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, HelpMessage = "Pasta raiz para buscar repositorios")]
    [ValidateScript({ Test-Path $_ -PathType Container })]
    [string]$Path,

    [Parameter(HelpMessage = "Pasta para armazenar backups")]
    [string]$BackupPath,

    [Parameter(HelpMessage = "Manter backups apos sucesso")]
    [switch]$KeepBackup,

    [Parameter(HelpMessage = "Simular sem executar")]
    [switch]$DryRun,

    [Parameter(HelpMessage = "Nao exigir remote configurado")]
    [switch]$SkipRemoteCheck,

    [Parameter(HelpMessage = "Desabilitar auto-commit")]
    [switch]$NoAutoCommit,

    [Parameter(HelpMessage = "Padroes de exclusao")]
    [string[]]$Exclude = @(),

    [Parameter(HelpMessage = "Arquivo de log")]
    [string]$LogFile
)

# ============================================================================
# CONFIGURACAO
# ============================================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "casa_git_compact.py"

# ============================================================================
# FUNCOES
# ============================================================================

function Write-Banner {
    $banner = @"

   ██████╗ █████╗ ███████╗ █████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔══██╗
  ██║     ███████║███████╗███████║
  ██║     ██╔══██║╚════██║██╔══██║
  ╚██████╗██║  ██║███████║██║  ██║
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
       GIT COMPACT v1.0
  
"@
    Write-Host $banner -ForegroundColor Magenta
}

function Write-Header {
    param([string]$Text)
    $line = "=" * 60
    Write-Host ""
    Write-Host $line -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor White
    Write-Host $line -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "[OK] $Text" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Text)
    Write-Host "[!!] $Text" -ForegroundColor Yellow
}

function Write-Err {
    param([string]$Text)
    Write-Host "[XX] $Text" -ForegroundColor Red
}

function Test-PythonVersion {
    try {
        $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonCmd) {
            $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
        }

        if (-not $pythonCmd) {
            return @{ Success = $false; Message = "Python nao encontrado no PATH"; Command = $null }
        }

        $versionOutput = & $pythonCmd.Source --version 2>&1
        if ($versionOutput -match "Python (\d+)\.(\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]

            if ($major -ge 3 -and $minor -ge 12) {
                return @{
                    Success = $true
                    Message = "Python $major.$minor encontrado"
                    Command = $pythonCmd.Source
                }
            }
            else {
                return @{
                    Success = $false
                    Message = "Python $major.$minor encontrado, mas e necessario 3.12+"
                    Command = $null
                }
            }
        }

        return @{ Success = $false; Message = "Nao foi possivel determinar a versao do Python"; Command = $null }
    }
    catch {
        return @{ Success = $false; Message = "Erro ao verificar Python: $_"; Command = $null }
    }
}

function Test-GitInstalled {
    try {
        $gitCmd = Get-Command git -ErrorAction SilentlyContinue
        if ($gitCmd) {
            $version = & git --version
            return @{ Success = $true; Message = $version }
        }
        return @{ Success = $false; Message = "Git nao encontrado no PATH" }
    }
    catch {
        return @{ Success = $false; Message = "Erro ao verificar Git: $_" }
    }
}

# ============================================================================
# VALIDACOES
# ============================================================================

Write-Banner
Write-Header "CASA GIT COMPACT - PowerShell Wrapper"

# Verificar se o script Python existe
if (-not (Test-Path $PythonScript)) {
    Write-Err "Script Python nao encontrado: $PythonScript"
    Write-Host "Certifique-se de que 'casa_git_compact.py' esta na mesma pasta que este script."
    exit 1
}
Write-Success "Script Python encontrado"

# Verificar Git
$gitCheck = Test-GitInstalled
if (-not $gitCheck.Success) {
    Write-Err $gitCheck.Message
    exit 1
}
Write-Success $gitCheck.Message

# Verificar Python
$pythonCheck = Test-PythonVersion
if (-not $pythonCheck.Success) {
    Write-Err $pythonCheck.Message
    Write-Host ""
    Write-Host "Instale Python 3.12 ou superior:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Cyan
    exit 1
}
Write-Success $pythonCheck.Message

# ============================================================================
# CONSTRUIR ARGUMENTOS
# ============================================================================

$pythonArgs = @(
    $PythonScript
    "-p", (Resolve-Path $Path).Path
)

if ($BackupPath) {
    $pythonArgs += "--backup-path", $BackupPath
}

if ($KeepBackup) {
    $pythonArgs += "--keep-backup"
}

if ($DryRun) {
    $pythonArgs += "--dry-run"
}

if ($SkipRemoteCheck) {
    $pythonArgs += "--skip-remote-check"
}

if ($NoAutoCommit) {
    $pythonArgs += "--no-auto-commit"
}

if ($Exclude.Count -gt 0) {
    $pythonArgs += "--exclude"
    $pythonArgs += $Exclude
}

if ($LogFile) {
    $pythonArgs += "--log-file", $LogFile
}

# ============================================================================
# EXECUTAR
# ============================================================================

Write-Host ""
Write-Host "Executando compactacao..." -ForegroundColor Cyan
Write-Host ""

try {
    & $pythonCheck.Command $pythonArgs
    $exitCode = $LASTEXITCODE
}
catch {
    Write-Err "Erro ao executar o script Python: $_"
    exit 1
}

# ============================================================================
# FINALIZACAO
# ============================================================================

Write-Host ""
if ($exitCode -eq 0) {
    Write-Success "Compactacao concluida com sucesso!"
}
else {
    Write-Warn "Compactacao concluida com alguns erros. Verifique o log."
}

exit $exitCode
