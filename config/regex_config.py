import json
import re
from pathlib import Path

# Caminho para o arquivo de configuracao de regex
CONFIG_FILE = Path(__file__).resolve().parent / "regex_patterns.json"


def load_patterns() -> dict:
    """Carrega e compila os padroes de regex a partir do JSON."""
    with open(CONFIG_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return {name: re.compile(pattern) for name, pattern in data.items()}


# Padroes carregados e compilados ao importar o modulo
PATTERNS = load_patterns()
