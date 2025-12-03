#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║                     CASA GIT COMPACT                          ║
║         Compacta repositorios Git com seguranca total         ║
║                       Python 3.12+                            ║
╚═══════════════════════════════════════════════════════════════╝
"""

import argparse
import logging
import subprocess
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path


# ============================================================================
# ENUMS E DATACLASSES
# ============================================================================

class RepoStatus(Enum):
    """Status de um repositorio durante o processo."""
    PENDING = auto()
    SKIPPED_LOCKED = auto()
    SKIPPED_CORRUPT = auto()
    SKIPPED_NO_REMOTE = auto()
    COMPACTED = auto()
    FAILED = auto()
    RESTORED = auto()


@dataclass
class GitRepository:
    """Representa um repositorio Git."""
    path: Path
    size_before: int = 0
    size_after: int = 0
    status: RepoStatus = RepoStatus.PENDING
    error_message: str = ""
    commit_count: int = 0
    branch_count: int = 0
    tag_count: int = 0
    auto_committed: bool = False

    @property
    def git_dir(self) -> Path:
        return self.path / ".git"

    @property
    def size_saved(self) -> int:
        return self.size_before - self.size_after


@dataclass
class CompactConfig:
    """Configuracoes da compactacao."""
    root_path: Path
    backup_path: Path | None = None
    keep_backup: bool = False
    dry_run: bool = False
    skip_remote_check: bool = False
    exclude_patterns: list[str] = field(default_factory=list)
    log_file: Path | None = None
    auto_commit: bool = True


@dataclass
class CompactSummary:
    """Resumo final da compactacao."""
    total_repos: int = 0
    compacted: int = 0
    skipped: int = 0
    failed: int = 0
    restored: int = 0
    auto_committed: int = 0
    total_size_before: int = 0
    total_size_after: int = 0

    @property
    def total_saved(self) -> int:
        return self.total_size_before - self.total_size_after


# ============================================================================
# GIT COMMAND RUNNER
# ============================================================================

class GitCommandRunner:
    """Executa comandos Git com tratamento de erros."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    def run(self, *args: str, check: bool = True, timeout: int = 600) -> subprocess.CompletedProcess:
        """Executa um comando git no repositorio."""
        cmd = ["git", "-C", str(self.repo_path), *args]
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout
        )

    def is_clean(self) -> bool:
        """Verifica se o repositorio esta limpo (sem alteracoes pendentes)."""
        result = self.run("status", "--porcelain", check=False)
        return result.returncode == 0 and not result.stdout.strip()

    def has_changes(self) -> bool:
        """Verifica se ha alteracoes nao commitadas."""
        return not self.is_clean()

    def has_remote(self) -> bool:
        """Verifica se ha remote configurado."""
        result = self.run("remote", "-v", check=False)
        return bool(result.stdout.strip())

    def fsck(self) -> tuple[bool, str]:
        """Verifica integridade do repositorio."""
        result = self.run("fsck", "--full", check=False)
        is_ok = result.returncode == 0
        return is_ok, result.stderr if not is_ok else ""

    def count_commits(self) -> int:
        """Conta o numero de commits."""
        result = self.run("rev-list", "--all", "--count", check=False)
        return int(result.stdout.strip()) if result.returncode == 0 else -1

    def count_branches(self) -> int:
        """Conta o numero de branches."""
        result = self.run("branch", "-a", check=False)
        if result.returncode != 0:
            return -1
        return len([b for b in result.stdout.strip().split("\n") if b.strip()])

    def count_tags(self) -> int:
        """Conta o numero de tags."""
        result = self.run("tag", check=False)
        if result.returncode != 0:
            return -1
        tags = result.stdout.strip()
        return len(tags.split("\n")) if tags else 0

    def create_bundle(self, bundle_path: Path) -> bool:
        """Cria um bundle completo do repositorio."""
        result = self.run("bundle", "create", str(bundle_path), "--all", check=False)
        return result.returncode == 0

    def apply_compression_config(self) -> bool:
        """Aplica configuracoes de compressao maxima."""
        configs = [
            ("core.compression", "9"),
            ("pack.compression", "9"),
            ("gc.aggressiveDepth", "250"),
            ("gc.aggressiveWindow", "250"),
        ]
        for key, value in configs:
            result = self.run("config", "--local", key, value, check=False)
            if result.returncode != 0:
                return False
        return True

    def compact(self) -> tuple[bool, str]:
        """Executa comandos de compactacao."""
        commands = [
            ("reflog", "expire", "--expire=now", "--all"),
            ("repack", "-a", "-d", "-f", "--depth=250", "--window=250"),
            ("gc", "--aggressive", "--prune=now"),
        ]
        for cmd in commands:
            result = self.run(*cmd, check=False)
            if result.returncode != 0:
                return False, f"Falha em 'git {' '.join(cmd)}': {result.stderr}"
        return True, ""

    def auto_commit(self) -> tuple[bool, str]:
        """Faz auto-commit de todas as alteracoes pendentes."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto Commit por CasaGitCompact [{timestamp}]"

        result_add = self.run("add", "-A", check=False)
        if result_add.returncode != 0:
            return False, f"Falha no git add: {result_add.stderr}"

        result_commit = self.run("commit", "-m", commit_message, check=False)
        if result_commit.returncode != 0:
            if "nothing to commit" in result_commit.stdout.lower():
                return True, "Nada para commitar"
            return False, f"Falha no git commit: {result_commit.stderr}"

        return True, commit_message


# ============================================================================
# REPOSITORY SCANNER
# ============================================================================

class RepositoryScanner:
    """Busca repositorios Git em uma pasta."""

    def __init__(self, exclude_patterns: list[str] | None = None):
        self.exclude_patterns = exclude_patterns or []

    def scan(self, root_path: Path) -> list[GitRepository]:
        """Busca todos os repositorios Git recursivamente."""
        repos = []
        for git_dir in root_path.rglob(".git"):
            if not git_dir.is_dir():
                continue

            repo_path = git_dir.parent

            if self._should_exclude(repo_path):
                continue

            repos.append(GitRepository(path=repo_path))

        return repos

    def _should_exclude(self, path: Path) -> bool:
        """Verifica se o caminho deve ser excluido."""
        path_str = str(path).lower()
        for pattern in self.exclude_patterns:
            if pattern.lower() in path_str:
                return True
        return False


# ============================================================================
# BACKUP MANAGER
# ============================================================================

class BackupManager:
    """Gerencia backups dos repositorios."""

    BACKUP_FOLDER_NAME = "_casa_git_compact_backups"

    def __init__(self, backup_root: Path | None = None):
        self.backup_root = backup_root

    def create_backup(self, repo: GitRepository) -> Path | None:
        """Cria backup do repositorio usando git bundle."""
        backup_dir = self._get_backup_dir(repo)
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bundle_name = f"{repo.path.name}_{timestamp}.bundle"
        bundle_path = backup_dir / bundle_name

        git = GitCommandRunner(repo.path)
        if git.create_bundle(bundle_path):
            return bundle_path
        return None

    def restore_backup(self, repo: GitRepository, bundle_path: Path) -> bool:
        """Restaura repositorio a partir do bundle."""
        if not bundle_path.exists():
            return False

        git_dir = repo.git_dir
        if git_dir.exists():
            temp_backup = git_dir.parent / f".git_corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.move(str(git_dir), str(temp_backup))

        try:
            temp_clone = repo.path.parent / f"_temp_restore_{repo.path.name}"
            subprocess.run(
                ["git", "clone", str(bundle_path), str(temp_clone)],
                capture_output=True,
                text=True,
                check=True
            )

            shutil.move(str(temp_clone / ".git"), str(git_dir))
            shutil.rmtree(str(temp_clone), ignore_errors=True)

            if temp_backup.exists():
                shutil.rmtree(str(temp_backup), ignore_errors=True)

            return True
        except Exception:
            if temp_backup.exists():
                shutil.move(str(temp_backup), str(git_dir))
            return False

    def remove_backup(self, bundle_path: Path) -> None:
        """Remove arquivo de backup."""
        if bundle_path.exists():
            bundle_path.unlink()

    def _get_backup_dir(self, repo: GitRepository) -> Path:
        """Retorna o diretorio de backup para o repositorio."""
        if self.backup_root:
            return self.backup_root
        return repo.path.parent / self.BACKUP_FOLDER_NAME


# ============================================================================
# REPOSITORY VALIDATOR
# ============================================================================

class RepositoryValidator:
    """Valida estado e integridade do repositorio."""

    def __init__(self, repo: GitRepository):
        self.repo = repo
        self.git = GitCommandRunner(repo.path)

    def has_lock_files(self) -> bool:
        """Verifica se ha arquivos .lock no repositorio."""
        git_dir = self.repo.git_dir
        lock_files = list(git_dir.glob("*.lock")) + list(git_dir.glob("**/*.lock"))
        return len(lock_files) > 0

    def validate_pre_compact(self, skip_remote_check: bool = False) -> tuple[bool, RepoStatus, str]:
        """Valida se o repositorio pode ser compactado."""
        if self.has_lock_files():
            return False, RepoStatus.SKIPPED_LOCKED, "Arquivos .lock encontrados"

        if not skip_remote_check and not self.git.has_remote():
            return False, RepoStatus.SKIPPED_NO_REMOTE, "Nenhum remote configurado"

        is_ok, error = self.git.fsck()
        if not is_ok:
            return False, RepoStatus.SKIPPED_CORRUPT, f"Falha no fsck: {error}"

        return True, RepoStatus.PENDING, ""

    def validate_post_compact(
        self,
        original_commits: int,
        original_branches: int,
        original_tags: int
    ) -> tuple[bool, str]:
        """Valida se a compactacao nao corrompeu o repositorio."""
        is_ok, error = self.git.fsck()
        if not is_ok:
            return False, f"Falha no fsck pos-compactacao: {error}"

        current_commits = self.git.count_commits()
        current_branches = self.git.count_branches()
        current_tags = self.git.count_tags()

        if current_commits != original_commits:
            return False, f"Contagem de commits diferente: {original_commits} -> {current_commits}"

        if current_branches != original_branches:
            return False, f"Contagem de branches diferente: {original_branches} -> {current_branches}"

        if current_tags != original_tags:
            return False, f"Contagem de tags diferente: {original_tags} -> {current_tags}"

        return True, ""


# ============================================================================
# COMPACTOR
# ============================================================================

class Compactor:
    """Executa a compactacao de um repositorio."""

    def __init__(
        self,
        backup_manager: BackupManager,
        keep_backup: bool = False,
        dry_run: bool = False,
        auto_commit: bool = True
    ):
        self.backup_manager = backup_manager
        self.keep_backup = keep_backup
        self.dry_run = dry_run
        self.auto_commit = auto_commit

    def compact(self, repo: GitRepository, skip_remote_check: bool = False) -> GitRepository:
        """Compacta um repositorio com todas as verificacoes de seguranca."""
        git = GitCommandRunner(repo.path)
        validator = RepositoryValidator(repo)

        repo.size_before = self._get_git_size(repo)

        # 0. Auto-commit se houver alteracoes pendentes
        if git.has_changes():
            if self.auto_commit:
                if self.dry_run:
                    repo.auto_committed = True
                else:
                    success, message = git.auto_commit()
                    if success:
                        repo.auto_committed = True
                    else:
                        repo.status = RepoStatus.FAILED
                        repo.error_message = f"Falha no auto-commit: {message}"
                        repo.size_after = repo.size_before
                        return repo

        # 1. Validacao pre-compactacao
        can_compact, status, message = validator.validate_pre_compact(skip_remote_check)
        if not can_compact:
            repo.status = status
            repo.error_message = message
            repo.size_after = repo.size_before
            return repo

        # 2. Salvar metricas originais
        repo.commit_count = git.count_commits()
        repo.branch_count = git.count_branches()
        repo.tag_count = git.count_tags()

        # Modo dry-run: apenas simula
        if self.dry_run:
            repo.status = RepoStatus.COMPACTED
            repo.size_after = repo.size_before
            repo.error_message = "[DRY-RUN] Simulacao apenas"
            return repo

        # 3. Criar backup
        bundle_path = self.backup_manager.create_backup(repo)
        if not bundle_path:
            repo.status = RepoStatus.FAILED
            repo.error_message = "Falha ao criar backup"
            repo.size_after = repo.size_before
            return repo

        try:
            # 4. Aplicar configuracoes
            if not git.apply_compression_config():
                raise Exception("Falha ao aplicar configuracoes de compressao")

            # 5. Executar compactacao
            success, error = git.compact()
            if not success:
                raise Exception(error)

            # 6. Validar pos-compactacao
            is_valid, validation_error = validator.validate_post_compact(
                repo.commit_count, repo.branch_count, repo.tag_count
            )
            if not is_valid:
                raise Exception(validation_error)

            # Sucesso!
            repo.status = RepoStatus.COMPACTED
            repo.size_after = self._get_git_size(repo)

            if not self.keep_backup:
                self.backup_manager.remove_backup(bundle_path)

        except Exception as e:
            repo.error_message = str(e)
            restored = self.backup_manager.restore_backup(repo, bundle_path)

            if restored:
                repo.status = RepoStatus.RESTORED
                repo.error_message += " | Backup restaurado com sucesso"
            else:
                repo.status = RepoStatus.FAILED
                repo.error_message += " | FALHA ao restaurar backup!"

            repo.size_after = self._get_git_size(repo)

        return repo

    def _get_git_size(self, repo: GitRepository) -> int:
        """Retorna o tamanho da pasta .git em bytes."""
        total = 0
        git_dir = repo.git_dir
        if git_dir.exists():
            for f in git_dir.rglob("*"):
                if f.is_file():
                    total += f.stat().st_size
        return total


# ============================================================================
# CASA LOGGER
# ============================================================================

class CasaLogger:
    """Logger com saida colorida e arquivo de log."""

    COLORS = {
        "RESET": "\033[0m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
        "CYAN": "\033[96m",
        "BOLD": "\033[1m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
    }

    BANNER = """
   ██████╗ █████╗ ███████╗ █████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔══██╗
  ██║     ███████║███████╗███████║
  ██║     ██╔══██║╚════██║██╔══██║
  ╚██████╗██║  ██║███████║██║  ██║
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
       GIT COMPACT v1.0
    """

    def __init__(self, log_file: Path | None = None):
        self.log_file = log_file
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configura o sistema de logging."""
        handlers: list[logging.Handler] = [logging.StreamHandler()]

        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(logging.FileHandler(self.log_file, encoding="utf-8"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=handlers
        )
        self.logger = logging.getLogger("CasaGitCompact")

    def banner(self) -> None:
        """Exibe o banner do programa."""
        self.logger.info(self._color("MAGENTA", self.BANNER))

    def header(self, text: str) -> None:
        """Exibe cabecalho."""
        line = "=" * 60
        self.logger.info(f"\n{self._color('CYAN', line)}")
        self.logger.info(f"{self._color('BOLD', text)}")
        self.logger.info(f"{self._color('CYAN', line)}")

    def info(self, text: str) -> None:
        self.logger.info(text)

    def success(self, text: str) -> None:
        self.logger.info(self._color("GREEN", f"[OK] {text}"))

    def warning(self, text: str) -> None:
        self.logger.info(self._color("YELLOW", f"[!!] {text}"))

    def error(self, text: str) -> None:
        self.logger.info(self._color("RED", f"[XX] {text}"))

    def commit_info(self, text: str) -> None:
        """Exibe info de auto-commit."""
        self.logger.info(self._color("BLUE", f"[>>] {text}"))

    def repo_result(self, repo: GitRepository) -> None:
        """Exibe resultado de um repositorio."""
        name = repo.path.name
        size_before = self._format_size(repo.size_before)
        size_after = self._format_size(repo.size_after)
        saved = self._format_size(repo.size_saved)

        if repo.auto_committed:
            self.commit_info(f"{name}: Auto-commit realizado")

        match repo.status:
            case RepoStatus.COMPACTED:
                self.success(f"{name}: {size_before} -> {size_after} (economia: {saved})")
            case RepoStatus.RESTORED:
                self.warning(f"{name}: Restaurado apos falha - {repo.error_message}")
            case RepoStatus.FAILED:
                self.error(f"{name}: FALHA - {repo.error_message}")
            case _:
                self.warning(f"{name}: Ignorado - {repo.error_message}")

    def summary(self, summary: CompactSummary) -> None:
        """Exibe resumo final."""
        self.header("RESUMO FINAL")
        self.info(f"Total de repositorios: {summary.total_repos}")
        self.success(f"Compactados: {summary.compacted}")
        if summary.auto_committed > 0:
            self.commit_info(f"Auto-commits realizados: {summary.auto_committed}")
        self.warning(f"Ignorados: {summary.skipped}")
        self.error(f"Falhas: {summary.failed}")
        if summary.restored > 0:
            self.warning(f"Restaurados: {summary.restored}")
        self.info("")
        self.info(f"Tamanho total antes: {self._format_size(summary.total_size_before)}")
        self.info(f"Tamanho total depois: {self._format_size(summary.total_size_after)}")
        self.success(f"Economia total: {self._format_size(summary.total_saved)}")

    def _color(self, color: str, text: str) -> str:
        """Aplica cor ao texto."""
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['RESET']}"

    def _format_size(self, size_bytes: int) -> str:
        """Formata tamanho em bytes para humano."""
        for unit in ["B", "KB", "MB", "GB"]:
            if abs(size_bytes) < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class CasaGitCompactApp:
    """Aplicacao principal que orquestra a compactacao."""

    def __init__(self, config: CompactConfig):
        self.config = config
        self.logger = CasaLogger(config.log_file)
        self.scanner = RepositoryScanner(config.exclude_patterns)
        self.backup_manager = BackupManager(config.backup_path)
        self.compactor = Compactor(
            self.backup_manager,
            keep_backup=config.keep_backup,
            dry_run=config.dry_run,
            auto_commit=config.auto_commit
        )

    def run(self) -> CompactSummary:
        """Executa a compactacao em todos os repositorios."""
        self.logger.banner()
        self.logger.header("CASA GIT COMPACT")
        self.logger.info(f"Pasta raiz: {self.config.root_path}")
        self.logger.info(f"Dry-run: {'Sim' if self.config.dry_run else 'Nao'}")
        self.logger.info(f"Manter backups: {'Sim' if self.config.keep_backup else 'Nao'}")
        self.logger.info(f"Auto-commit: {'Sim' if self.config.auto_commit else 'Nao'}")

        self.logger.info("\nBuscando repositorios...")
        repos = self.scanner.scan(self.config.root_path)
        self.logger.info(f"Encontrados: {len(repos)} repositorios\n")

        if not repos:
            self.logger.warning("Nenhum repositorio encontrado!")
            return CompactSummary()

        summary = CompactSummary(total_repos=len(repos))

        for i, repo in enumerate(repos, 1):
            self.logger.info(f"\n[{i}/{len(repos)}] Processando: {repo.path}")

            repo = self.compactor.compact(repo, self.config.skip_remote_check)
            self.logger.repo_result(repo)

            summary.total_size_before += repo.size_before
            summary.total_size_after += repo.size_after

            if repo.auto_committed:
                summary.auto_committed += 1

            match repo.status:
                case RepoStatus.COMPACTED:
                    summary.compacted += 1
                case RepoStatus.RESTORED:
                    summary.restored += 1
                case RepoStatus.FAILED:
                    summary.failed += 1
                case _:
                    summary.skipped += 1

        self.logger.summary(summary)
        return summary


# ============================================================================
# CLI
# ============================================================================

def parse_args() -> CompactConfig:
    """Parse argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="CASA GIT COMPACT - Compacta repositorios Git com seguranca.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python casa_git_compact.py -p C:\\Projetos
  python casa_git_compact.py -p /home/user/repos --dry-run
  python casa_git_compact.py -p . --keep-backup --backup-path D:\\Backups
  python casa_git_compact.py -p . --no-auto-commit
        """
    )

    parser.add_argument(
        "-p", "--path",
        type=Path,
        required=True,
        help="Pasta raiz para buscar repositorios"
    )
    parser.add_argument(
        "--backup-path",
        type=Path,
        help="Pasta para armazenar backups (padrao: junto ao repo)"
    )
    parser.add_argument(
        "--keep-backup",
        action="store_true",
        help="Manter backups mesmo apos sucesso"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular sem executar alteracoes"
    )
    parser.add_argument(
        "--skip-remote-check",
        action="store_true",
        help="Nao exigir remote configurado"
    )
    parser.add_argument(
        "--no-auto-commit",
        action="store_true",
        help="Desabilitar auto-commit de alteracoes pendentes"
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Padroes de exclusao (ex: backup temp)"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Arquivo de log"
    )

    args = parser.parse_args()

    return CompactConfig(
        root_path=args.path.resolve(),
        backup_path=args.backup_path.resolve() if args.backup_path else None,
        keep_backup=args.keep_backup,
        dry_run=args.dry_run,
        skip_remote_check=args.skip_remote_check,
        exclude_patterns=args.exclude,
        log_file=args.log_file.resolve() if args.log_file else None,
        auto_commit=not args.no_auto_commit,
    )


def main() -> int:
    """Ponto de entrada principal."""
    try:
        config = parse_args()
        app = CasaGitCompactApp(config)
        summary = app.run()

        if summary.failed > 0:
            return 1
        return 0

    except KeyboardInterrupt:
        print("\n\nOperacao cancelada pelo usuario.")
        return 130
    except Exception as e:
        print(f"\nErro fatal: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
