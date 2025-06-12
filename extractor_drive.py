"""Entry point for running PII extraction and exporting results."""

import logging
import os

from pii_extractor import (
    extrair_e_processar_zip,
    exportar_resultados_csv,
    exportar_resultados_json,
    exportar_resultados_sqlite,
)
from normalization import normalize_results


def main() -> None:
    zip_file = os.getenv("ZIP_INPUT", "columbiati.zip")
    resultados = extrair_e_processar_zip(zip_file)

    # Normalize extracted values before exporting
    resultados = normalize_results(resultados)

    exportar_resultados_csv(resultados, caminho_csv="resultados.csv")
    exportar_resultados_json(resultados, caminho_json="resultados.json")
    exportar_resultados_sqlite(resultados, db_path="resultados.db")
    logging.info("Exportação concluída: CSV, JSON e SQLite.")


if __name__ == "__main__":
    main()
