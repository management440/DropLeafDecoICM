import logging
import os
import shutil
import subprocess
from datetime import datetime

from modules.marketplace_integration.export_module import run_export

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXPORT_DIR = os.path.join(REPO_ROOT, "02_export")
ARCHIVE_DIR = os.path.join(REPO_ROOT, "03_archive")

ALLOWED_STAGE_PREFIXES = (
    os.path.normcase(os.path.join(REPO_ROOT, "02_export")),
    os.path.normcase(os.path.join(REPO_ROOT, "03_archive")),
)


def _git(*args) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def _archive_csv(csv_path: str) -> str:
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    dest = os.path.join(ARCHIVE_DIR, os.path.basename(csv_path))
    shutil.move(csv_path, dest)
    log.info("Archived %s → %s", csv_path, dest)
    return dest


def _check_staged_files():
    """Abort if staged files fall outside the allowed directories."""
    staged = _git("diff", "--cached", "--name-only")
    if not staged:
        return
    unexpected = []
    for rel_path in staged.splitlines():
        abs_path = os.path.normcase(os.path.join(REPO_ROOT, rel_path))
        if not any(abs_path.startswith(prefix) for prefix in ALLOWED_STAGE_PREFIXES):
            unexpected.append(rel_path)
    if unexpected:
        _git("reset", "HEAD")
        raise RuntimeError(
            f"Aborting push — unexpected files staged: {unexpected}. "
            "Commit these manually or update .gitignore."
        )


def orchestrate_export() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log.info("Step 1: Running export…")
    csv_path = run_export()
    log.info("Export complete: %s", csv_path)

    log.info("Step 2: Archiving CSV to 03_archive/…")
    archived_path = _archive_csv(csv_path)

    log.info("Step 3: Staging export and archive directories…")
    _git("add", EXPORT_DIR, ARCHIVE_DIR)

    log.info("Step 4: Dry-run guard — checking staged files…")
    _check_staged_files()
    log.info("Guard passed — all staged files are within allowed paths.")

    log.info("Step 5: Committing…")
    commit_msg = f"Automated archive: {timestamp}"
    _git("commit", "-m", commit_msg)
    log.info("Committed: %s", commit_msg)

    log.info("Step 6: Pushing to remote…")
    _git("push")
    log.info("Push complete.")

    return archived_path
