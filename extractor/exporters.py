import os
import csv
import json
import sqlite3
from typing import Dict, Any


def export_csv(resultados: Dict[str, Any], caminho: str = "data/resultados.csv") -> None:
    """Exporta os resultados para um arquivo CSV."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["arquivo", "origem", "tipo", "valor"])
        for arquivo, dados in resultados.items():
            for origem in ["regex", "gpt"]:
                info = dados.get(origem)
                if isinstance(info, dict):
                    for tipo, valores in info.items():
                        if isinstance(valores, list):
                            for valor in valores:
                                writer.writerow([arquivo, origem, tipo, valor])
                        else:
                            writer.writerow([arquivo, origem, tipo, valores])
                else:
                    writer.writerow([arquivo, origem, "conteudo", info])


def export_json(resultados: Dict[str, Any], caminho: str = "data/resultados.json") -> None:
    """Exporta os resultados para um arquivo JSON."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)


def export_sqlite(resultados: Dict[str, Any], db_path: str = "data/resultados.db") -> None:
    """Exporta os resultados para um banco de dados SQLite."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dados (
            arquivo TEXT,
            origem TEXT,
            tipo TEXT,
            valor TEXT
        )
        """
    )
    for arquivo, dados in resultados.items():
        for origem in ["regex", "gpt"]:
            info = dados.get(origem)
            if isinstance(info, dict):
                for tipo, valores in info.items():
                    if isinstance(valores, list):
                        for valor in valores:
                            cursor.execute(
                                "INSERT INTO dados VALUES (?, ?, ?, ?)",
                                (arquivo, origem, tipo, valor),
                            )
                    else:
                        cursor.execute(
                            "INSERT INTO dados VALUES (?, ?, ?, ?)",
                            (arquivo, origem, tipo, valores),
                        )
            else:
                cursor.execute(
                    "INSERT INTO dados VALUES (?, ?, ?, ?)",
                    (arquivo, origem, "conteudo", info),
                )
    conn.commit()
    conn.close()
