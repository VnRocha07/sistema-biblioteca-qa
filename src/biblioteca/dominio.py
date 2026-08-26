"""Regras de emprestimo da Biblioteca Municipal.

Os nomes de funcao e constante sao os mesmos usados no material das aulas.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta

# prazo de emprestimo, em dias, por categoria de leitor
PRAZO = {"comum": 14, "estudante": 21, "professor": 30, "infantil": 7}

MULTA_DIA = 0.50       # valor da multa por dia de atraso
TETO_MULTA = 20.00     # teto da multa por emprestimo
LIMITE_MULTA = 15.00   # acima disto, o leitor nao retira novo exemplar
MAX_EM_MAOS = 3        # maximo de exemplares em maos por leitor


@dataclass
class Emprestimo:
    codigo_exemplar: str
    leitor_id: int
    categoria: str
    data_emprestimo: date
    data_prevista: date = field(init=False)
    data_devolucao: date | None = None

    def __post_init__(self) -> None:
        # se a categoria nao existir, isto levanta KeyError -- e nao um
        # erro de negocio com mensagem compreensivel.
        self.data_prevista = self.data_emprestimo + timedelta(days=PRAZO[self.categoria])


def dias_atraso(emp: Emprestimo, hoje: date) -> int:
    ref = emp.data_devolucao or hoje
    return max(0, (ref - emp.data_prevista).days)


def calcular_multa(emp: Emprestimo, hoje: date) -> float:
    return min(dias_atraso(emp, hoje) * MULTA_DIA, TETO_MULTA)


def pode_emprestar(leitor_id: int, multa_acumulada: float, exemplares_em_maos: int) -> bool:
    if multa_acumulada > LIMITE_MULTA:
        return False
    if exemplares_em_maos >= MAX_EM_MAOS:
        return False
    return True


def multa_com_regras_especiais(emp: Emprestimo, hoje: date, feriados: list[date],
                               categoria_isenta: bool, em_campanha_perdao: bool,
                               reincidente: bool) -> float:
    dias = dias_atraso(emp, hoje)
    if categoria_isenta:
        return 0.0
    if em_campanha_perdao and dias < 30:
        return 0.0
    for f in feriados:
        if emp.data_prevista <= f <= hoje:
            dias -= 1
    if dias <= 0:
        return 0.0
    valor = dias * MULTA_DIA
    if reincidente:
        valor *= 1.5
    if emp.categoria == "infantil" and valor > 5:
        valor = 5.0
    return min(valor, TETO_MULTA)
