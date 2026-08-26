"""Conexao com o banco de dados de laboratorio (SQLite)."""
from __future__ import annotations
import sqlite3
from pathlib import Path

CAMINHO_PADRAO = Path("acervo.db")
ESQUEMA = Path(__file__).resolve().parents[2] / "esquema"


def conectar(caminho: str | Path = CAMINHO_PADRAO) -> sqlite3.Connection:
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    # ATENCAO: o SQLite nao verifica chave estrangeira por padrao.
    # A linha abaixo esta COMENTADA de proposito -- faz parte do que
    # a auditoria da UA 4 deve avaliar.
    # conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_esquema(conn: sqlite3.Connection) -> None:
    conn.executescript((ESQUEMA / "01-schema.sql").read_text(encoding="utf-8"))


def carregar_dados(conn: sqlite3.Connection) -> None:
    conn.executescript((ESQUEMA / "02-carga.sql").read_text(encoding="utf-8"))
