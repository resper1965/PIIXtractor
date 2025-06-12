import os
import zipfile
import logging
import shutil
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from extractor.exporters import export_csv, export_json, export_sqlite
from search.process import process_directory

# --- Initial Configuration ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

TMP_ROOT = Path("tmp")




def extrair_e_processar_zip(zip_path: str) -> Dict[str, Any]:
    """Extrai arquivos de um ZIP e processa seu conteúdo."""
    tmpdir = TMP_ROOT / "piiextractor_tmp"
    tmpdir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
            logging.info(f"ZIP extraído em: {tmpdir}")
    except Exception as e:
        logging.error(f"[ERRO ao extrair ZIP] {e}")
        return {}

    resultados = process_directory(str(tmpdir))

    try:
        shutil.rmtree(tmpdir)
        logging.info(f"Diretório temporário removido: {tmpdir}")
    except Exception as e:
        logging.warning(f"Falha ao remover tmpdir: {e}")

    return resultados


if __name__ == "__main__":
    zip_file = os.getenv("ZIP_INPUT", "columbiati.zip")
    resultados = extrair_e_processar_zip(zip_file)

    for arq, info in resultados.items():
        print(f"\n\U0001F4C4 {arq}")
        print("Regex:", info["regex"])
        print("GPT:", info["gpt"])

    export_csv(resultados, caminho="resultados.csv")
    export_json(resultados, caminho="resultados.json")
    export_sqlite(resultados, db_path="resultados.db")
    logging.info("Exportação concluída: CSV, JSON e SQLite.")

    try:
        shutil.rmtree(TMP_ROOT)
        logging.info(f"Diretório temporário removido: {TMP_ROOT}")
    except Exception as e:
        logging.warning(f"Falha ao remover diretório temporário '{TMP_ROOT}': {e}")
