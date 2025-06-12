import csv
import json
import sqlite3
from extractor.exporters import export_csv, export_json, export_sqlite

SAMPLE_RESULTS = {
    "file1.txt": {
        "regex": {"email": ["a@test.com"], "cpf": ["123"]},
        "gpt": "Detected PII",
    }
}


def test_export_csv(tmp_path):
    out = tmp_path / "out.csv"
    export_csv(SAMPLE_RESULTS, caminho=str(out))
    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["arquivo", "origem", "tipo", "valor"]
    assert sorted(rows[1:]) == sorted([
        ["file1.txt", "regex", "email", "a@test.com"],
        ["file1.txt", "regex", "cpf", "123"],
        ["file1.txt", "gpt", "conteudo", "Detected PII"],
    ])


def test_export_json(tmp_path):
    out = tmp_path / "out.json"
    export_json(SAMPLE_RESULTS, caminho=str(out))
    with open(out, encoding="utf-8") as f:
        data = json.load(f)
    assert data == SAMPLE_RESULTS


def test_export_sqlite(tmp_path):
    db = tmp_path / "out.db"
    export_sqlite(SAMPLE_RESULTS, db_path=str(db))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT arquivo, origem, tipo, valor FROM dados")
    rows = sorted(cursor.fetchall())
    conn.close()
    assert rows == sorted([
        ("file1.txt", "regex", "email", "a@test.com"),
        ("file1.txt", "regex", "cpf", "123"),
        ("file1.txt", "gpt", "conteudo", "Detected PII"),
    ])
