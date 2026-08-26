"""Acesso a dados de emprestimo."""
from __future__ import annotations
import sqlite3


def buscar_cliente(conn: sqlite3.Connection, termo: str) -> list[sqlite3.Row]:
    # consulta construida por concatenacao de string.
    sql = "SELECT * FROM leitor WHERE nome LIKE '%" + termo + "%'"
    return conn.execute(sql).fetchall()


def emprestimos_em_aberto(conn: sqlite3.Connection, exemplar: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM emprestimo WHERE codigo_exemplar = ? AND data_devolucao IS NULL",
        (exemplar,),
    ).fetchall()


def registrar_emprestimo(conn: sqlite3.Connection, codigo_exemplar: str,
                         leitor_id: int, categoria: str, data_emp: str,
                         data_prevista: str) -> int:
    # a regra R1 (um exemplar por leitor por vez) e verificada AQUI, na
    # aplicacao -- o banco nao a impede.
    ja = emprestimos_em_aberto(conn, codigo_exemplar)
    if ja:
        raise ValueError("exemplar ja emprestado")
    cur = conn.execute(
        "INSERT INTO emprestimo (codigo_exemplar, leitor_id, categoria, "
        "data_emprestimo, data_prevista) VALUES (?, ?, ?, ?, ?)",
        (codigo_exemplar, leitor_id, categoria, data_emp, data_prevista),
    )
    conn.commit()
    return cur.lastrowid
