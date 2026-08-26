"""Gera dados ficticios para o acervo, com volumetria de laboratorio.

Reduzido em relacao a volumetria real do dominio (18.400 titulos etc.) para
caber em um repositorio; a proporcao entre as tabelas e mantida. Nenhum dado
e de pessoa real.
"""
from __future__ import annotations
import sys
from datetime import date, timedelta

# gerador deterministico proprio, para nao depender de random (que a
# volumetria de laboratorio nao exige e que dificultaria reproducao)
def _seq(n, base):
    return [(base + i) for i in range(n)]

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elena", "Fabio", "Gisele",
         "Hugo", "Igor", "Julia", "Karla", "Lucas", "Marina", "Nilo",
         "Olga", "Paulo", "Rita", "Sergio", "Tania", "Vera"]
SOBRE = ["Souza", "Lima", "Dias", "Melo", "Rocha", "Nunes", "Alves",
         "Prado", "Gomes", "Reis"]
CATS = ["comum", "estudante", "professor", "infantil"]
PRAZO = {"comum": 14, "estudante": 21, "professor": 30, "infantil": 7}

def esc(s): return s.replace("'", "''")

def gerar(n_titulos=200, n_exemplares=500, n_leitores=200, n_emprestimos=1000):
    linhas = []
    # titulos -- alguns com ISBN duplicado de proposito (o esquema nao impede)
    for i in _seq(n_titulos, 1):
        isbn = f"978850100{(i % 180):04d}"   # colide a cada 180: duplicata
        linhas.append(f"INSERT INTO titulo VALUES ({i}, 'Titulo {i}', "
                      f"'Autor {i % 50}', '{isbn}');")
    # exemplares
    for i in _seq(n_exemplares, 1):
        t = (i % n_titulos) + 1
        linhas.append(f"INSERT INTO exemplar VALUES ('EX-{i:05d}', {t}, 'disponivel');")
    # leitores
    for i in _seq(n_leitores, 1):
        nome = f"{NOMES[i % len(NOMES)]} {SOBRE[(i // len(NOMES)) % len(SOBRE)]}"
        cat = CATS[i % len(CATS)]
        linhas.append(f"INSERT INTO leitor VALUES ({i}, '{esc(nome)}', "
                      f"'81 9{i:04d}-{(i*7) % 10000:04d}', '{cat}');")
    # emprestimos -- inclui denormalizacao (nome/telefone do leitor)
    base = date(2026, 6, 1)
    for i in _seq(n_emprestimos, 1):
        ex = f"EX-{((i % n_exemplares) + 1):05d}"
        lid = (i % n_leitores) + 1
        cat = CATS[lid % len(CATS)]
        nome = f"{NOMES[lid % len(NOMES)]} {SOBRE[(lid // len(NOMES)) % len(SOBRE)]}"
        d0 = base + timedelta(days=i % 80)
        d1 = d0 + timedelta(days=PRAZO[cat])
        dev = "NULL" if i % 6 == 0 else f"'{(d1 - timedelta(days=2)).isoformat()}'"
        linhas.append(
            f"INSERT INTO emprestimo (emprestimo_id, codigo_exemplar, leitor_id, "
            f"categoria, leitor_nome, leitor_telefone, data_emprestimo, "
            f"data_prevista, data_devolucao) VALUES "
            f"({i}, '{ex}', {lid}, '{cat}', '{esc(nome)}', '81 9{lid:04d}-0000', "
            f"'{d0.isoformat()}', '{d1.isoformat()}', {dev});")
    return "\n".join(linhas) + "\n"

if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "esquema/02-carga.sql"
    with open(dest, "w", encoding="utf-8") as f:
        f.write("-- Dados ficticios gerados por scripts/gerar_dados.py\n")
        f.write(gerar())
    print(f"gerado: {dest}")
