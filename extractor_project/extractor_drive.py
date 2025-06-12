import os
import argparse
import logging

from pii_extractor import processar_diretorio
from utils.file_manager import extract_zip, clean_directory
from extractor.exporters import export_csv, export_json, export_sqlite

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
DATA_DIR = os.path.join(BASE_DIR, 'data')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')


def extract_zip_wrapper(zip_path: str) -> str:
    """Legacy wrapper to keep script compatibility."""
    return str(extract_zip(zip_path, TMP_DIR) or TMP_DIR)


def clean_tmp() -> None:
    clean_directory(TMP_DIR)


def run_pipeline(zip_file: str) -> None:
    extract_zip_wrapper(zip_file)
    results = processar_diretorio(TMP_DIR)
    os.makedirs(DATA_DIR, exist_ok=True)
    export_csv(results, os.path.join(DATA_DIR, 'resultados.csv'))
    export_json(results, os.path.join(DATA_DIR, 'resultados.json'))
    export_sqlite(results, os.path.join(DATA_DIR, 'resultados.db'))
    clean_tmp()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PII extraction pipeline')
    parser.add_argument('zipfile', help='Path to zip file with documents')
    args = parser.parse_args()
    run_pipeline(args.zipfile)
