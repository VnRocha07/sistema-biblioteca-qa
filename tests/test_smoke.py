"""Teste de fumaca: o sistema sobe e as funcoes basicas respondem.

Este e o UNICO teste que acompanha o sistema. Construir a suite de testes que
expoe os defeitos e o trabalho da disciplina -- comece pela lista da aula.
"""
import sys, sqlite3
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from biblioteca.dominio import Emprestimo, calcular_multa, pode_emprestar
from biblioteca import db, repositorio as repo


def test_dominio_sobe():
    e = Emprestimo("EX-00001", 1, "estudante", date(2026, 8, 3))
    assert e.data_prevista == date(2026, 8, 24)
    assert calcular_multa(e, e.data_prevista) == 0.0
    assert pode_emprestar(1, 0.0, 0) is True


def test_banco_sobe(tmp_path):
    conn = db.conectar(tmp_path / "acervo.db")
    db.criar_esquema(conn)
    db.carregar_dados(conn)
    n = conn.execute("SELECT COUNT(*) FROM emprestimo").fetchone()[0]
    assert n > 0
    conn.close()


def test_registrar_emprestimo(tmp_path):
    conn = db.conectar(tmp_path / "acervo.db")
    db.criar_esquema(conn)
    hoje = date(2026, 9, 1)
    eid = repo.registrar_emprestimo(
        conn, "EX-00001", 1, "comum",
        hoje.isoformat(), (hoje + timedelta(days=14)).isoformat())
    assert eid > 0
    conn.close()
