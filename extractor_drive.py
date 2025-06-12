import os
import logging

from pii_extractor import extrair_e_processar_zip
from extractor.exporters import export_csv, export_json, export_sqlite


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main(zip_file: str) -> None:
    """Processa o ZIP informado e exporta os resultados."""
    resultados = extrair_e_processar_zip(zip_file)
    export_csv(resultados)
    export_json(resultados)
    export_sqlite(resultados)
    logging.info("Exportação concluída: CSV, JSON e SQLite")


if __name__ == "__main__":
    zip_file = os.getenv("ZIP_INPUT", "columbiati.zip")
    main(zip_file)
