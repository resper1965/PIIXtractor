import os
import argparse
import zipfile
import logging
import shutil

from pii_extractor import (
    processar_diretorio,
    exportar_resultados_csv,
    exportar_resultados_json,
    exportar_resultados_sqlite,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
DATA_DIR = os.path.join(BASE_DIR, 'data')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')


def extract_zip(zip_path: str) -> str:
    os.makedirs(TMP_DIR, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(TMP_DIR)
    logging.info('ZIP extracted to %s', TMP_DIR)
    return TMP_DIR


def clean_tmp() -> None:
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)


def run_pipeline(zip_file: str) -> None:
    extract_zip(zip_file)
    results = processar_diretorio(TMP_DIR)
    os.makedirs(DATA_DIR, exist_ok=True)
    exportar_resultados_csv(results, os.path.join(DATA_DIR, 'resultados.csv'))
    exportar_resultados_json(results, os.path.join(DATA_DIR, 'resultados.json'))
    exportar_resultados_sqlite(results, os.path.join(DATA_DIR, 'resultados.db'))
    clean_tmp()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PII extraction pipeline')
    parser.add_argument('zipfile', help='Path to zip file with documents')
    args = parser.parse_args()
    run_pipeline(args.zipfile)
