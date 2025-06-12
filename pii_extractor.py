import os

import re
=======
import zipfile

import logging
import time
from extractor.exporters import export_csv, export_json, export_sqlite
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from docx import Document
from openpyxl import load_workbook
from PyPDF2 import PdfReader
from extractor.openai_classifier import classify_text
from tqdm import tqdm

from utils.file_manager import extract_zip, clean_directory
=======
from config.regex_config import PATTERNS
from validation import validar_cpf, validar_cnpj


# --- Initial Configuration ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

TMP_ROOT = Path("tmp")


def extrair_texto_arquivo(caminho: str) -> str:
    """Lê e retorna o conteúdo de arquivos suportados."""
    try:
        if caminho.endswith(".txt"):
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        if caminho.endswith(".pdf"):
            reader = PdfReader(caminho)
            return "\n".join([p.extract_text() or "" for p in reader.pages])
        if caminho.endswith(".docx"):
            doc = Document(caminho)
            return "\n".join([p.text for p in doc.paragraphs])
        if caminho.endswith(".xlsx"):
            wb = load_workbook(caminho)
            dados = []
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    dados.append(" ".join([str(c) for c in row if c]))
            return "\n".join(dados)
    except Exception as e:
        logging.warning(f"[ERRO] {caminho}: {e}")
    return ""


def extrair_regex(texto: str) -> Dict[str, Any]:
    """Extrai dados utilizando regex."""
    resultado = {}
    for tipo, pattern in PATTERNS.items():
        encontrados = pattern.findall(texto)
        if tipo == "cpf":
            encontrados = [v for v in encontrados if validar_cpf(v)]
        elif tipo == "cnpj":
            encontrados = [v for v in encontrados if validar_cnpj(v)]
        if encontrados:
            resultado[tipo] = sorted(set(encontrados))
    return resultado




@dataclass
class Progresso:
    total: int
    barra: tqdm

    @classmethod
    def criar(cls, total: int) -> 'Progresso':
        barra = tqdm(total=total, desc="Processando arquivos", unit="arquivo")
        return cls(total=total, barra=barra)

    def atualizar(self):
        self.barra.update(1)

    def finalizar(self):
        self.barra.close()


def processar_diretorio(diretorio: str) -> Dict[str, Any]:
    """Processa todos os arquivos do diretório informado."""
    todos_arquivos = [os.path.join(r, f)
                      for r, _, files in os.walk(diretorio)
                      for f in files
                      if f.lower().endswith((".txt", ".pdf", ".docx", ".xlsx"))]
    progresso = Progresso.criar(len(todos_arquivos))

    resultados = {}
    for caminho in todos_arquivos:
        logging.info(f"Processando: {caminho}")
        texto = extrair_texto_arquivo(caminho)
        if not texto.strip():
            progresso.atualizar()
            continue
        if len(texto) > 50000:
            logging.warning(f"[SKIP] {caminho} excede 50k caracteres. Ignorando.")
            progresso.atualizar()
            continue
        regex_result = extrair_regex(texto)
        gpt_result = ""
        if not regex_result:
            gpt_result = classify_text(texto)
        resultados[caminho] = {
            "regex": regex_result,
            "gpt": gpt_result
        }
        progresso.atualizar()
        time.sleep(2)

    progresso.finalizar()
    return resultados




def extrair_e_processar_zip(zip_path: str) -> Dict[str, Any]:
    """Extrai arquivos de um ZIP e processa seu conteúdo."""
    tmpdir = TMP_ROOT / "piiextractor_tmp"

    extracted = extract_zip(zip_path, str(tmpdir))
    if extracted is None:
        return {}

    resultados = processar_diretorio(str(extracted))

    clean_directory(extracted)
    clean_directory(TMP_ROOT)

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

    clean_directory(TMP_ROOT)
