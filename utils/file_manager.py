import logging
import zipfile
import shutil
from pathlib import Path
from typing import Optional


def extract_zip(zip_path: str, dest_dir: str) -> Optional[Path]:
    """Extract ``zip_path`` into ``dest_dir``.

    The destination directory is created if it does not exist. Returns the
    path to the extracted directory or ``None`` if extraction failed.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dest)
        logging.info("ZIP extraído em: %s", dest)
        return dest
    except Exception as e:  # pragma: no cover - simple logging
        logging.error("[ERRO ao extrair ZIP] %s", e)
        return None


def clean_directory(path: str | Path) -> None:
    """Remove a directory and its contents, ignoring errors."""
    p = Path(path)
    try:
        if p.exists():
            shutil.rmtree(p)
            logging.info("Diretório removido: %s", p)
    except Exception as e:  # pragma: no cover - simple logging
        logging.warning("Falha ao remover diretório '%s': %s", p, e)
