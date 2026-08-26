# 📚 sistema-biblioteca-qa

Sistema de empréstimos da **Biblioteca Municipal**. É o software **sob auditoria** de
duas disciplinas do Prof. Petros Barreto, na UNIFG:

- **Garantia da Qualidade de Software** — audita o sistema inteiro
- **Banco de Dados** — modela e audita a camada de dados

> ⚠️ **Este sistema tem fragilidades reais**, por simplificação didática e por ser um
> ponto de partida que não foi escrito com rigor. **Encontrá-las e prová-las é o
> trabalho do semestre.** Não há aqui nenhuma lista dos problemas — é você quem os
> descobre, com evidência de reprodução.

---

## O domínio: a Biblioteca Municipal

```
  4 unidades          sede + tres bairros
  18.400 titulos      livro, periodico, midia
  31.200 exemplares   copias fisicas
  9.700 leitores      ativos, em quatro categorias
  380 emprestimos     por dia; pico de 1.100 na volta as aulas
  22 funcionarios     papeis diferentes veem dados diferentes
```

> A carga de dados deste repositório é **reduzida** (200 títulos, 500 exemplares, 200
> leitores, 1.000 empréstimos) para caber no repositório, mantendo a proporção entre as
> tabelas. Para gerar mais volume, use `scripts/gerar_dados.py`.

### As oito regras de negócio

| # | Regra |
|---|---|
| R1 | um exemplar só pode estar emprestado a um leitor por vez |
| R2 | o prazo depende da categoria do leitor **e** do tipo de título |
| R3 | leitor com multa acima do limite não retira novo exemplar |
| R4 | reserva vira empréstimo quando o exemplar é devolvido |
| R5 | periódico não tem ISBN; livro tem, e é único |
| R6 | o histórico de empréstimo nunca é apagado |
| R7 | exemplar danificado sai de circulação sem sair do acervo |
| R8 | o mesmo título pode ter exemplares em unidades diferentes |

⚠️ **Ao ler o código e o esquema, pergunte de cada regra: o sistema a garante? E onde
— no banco, ou só na aplicação?** Essa é a pergunta central da auditoria.

---

## Estrutura

```
src/biblioteca/
├── dominio.py       regras de emprestimo (Emprestimo, calcular_multa, ...)
├── repositorio.py   acesso a dados
└── db.py            conexao com o banco

esquema/
├── 01-schema.sql    o esquema do acervo (SQLite)
└── 02-carga.sql     dados ficticios gerados

scripts/
└── gerar_dados.py   gera a carga ficticia, com volume ajustavel

tests/
└── test_smoke.py    o UNICO teste que acompanha o sistema
```

---

## Como rodar

```bash
# 1. clonar o SEU fork
git clone https://github.com/SEU-USUARIO/sistema-biblioteca-qa.git
cd sistema-biblioteca-qa

# 2. ambiente
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. o teste de fumaca (deve passar)
pytest -q

# 4. subir o banco e explorar
python3 - <<'EOF'
from src.biblioteca import db
conn = db.conectar("acervo.db")
db.criar_esquema(conn)
db.carregar_dados(conn)
print("emprestimos:", conn.execute("SELECT COUNT(*) FROM emprestimo").fetchone()[0])
EOF

# 5. abrir o banco no DB Browser for SQLite (aulas 01-05 de Banco de Dados)
#    ou no psql, depois de portar o esquema para PostgreSQL (aula 06+)
```

---

## O que cada disciplina faz com este sistema

### Garantia da Qualidade de Software

O sistema é o alvo da **Auditoria de Qualidade**. Ao longo do semestre você:

```
M1  plano de teste + analise de risco sobre ESTE sistema
M2  inspecao e revisao, com defeitos registrados e PROVADOS
M3  casos de teste por tecnica
M4  suite automatizada nos 4 niveis + TDD de funcionalidade nova
M5  painel de metricas
M6  pipeline de CI com quality gates + parecer etico
M7  apresentacao do relatorio de auditoria
```

O núcleo de regras em `dominio.py` — `Emprestimo`, `dias_atraso`, `calcular_multa`,
`pode_emprestar` — é o mesmo trabalhado nas aulas.

### Banco de Dados

O esquema é a base do projeto **Acervo**. Você:

```
B1  modelo conceitual (DER) e dicionario de dados
B2  modelo logico e fisico, DDL executavel, 20 consultas
B3  normalizacao ate BCNF e o LAUDO DE ANOMALIAS deste esquema
B4  transacoes, isolamento, anomalias de concorrencia
...
```

⚠️ **O esquema deste repositório tem decisões discutíveis.** No B3, cada anomalia que
você apontar precisa ser **provada** — com a dependência funcional que a viola e o
comando que produz a inconsistência.

---

## Regras não negociáveis

**Achado sem prova de reprodução não conta.** Um defeito precisa vir com os passos que o
expõem — o comando, a entrada, o resultado.

**Achado fabricado zera a entrega.** O valor de um relatório de auditoria é inteiramente
a confiança em quem o escreveu.

**Nenhum dado real.** Todos os dados aqui são fictícios. Não acrescente nome, telefone,
endereço ou documento de pessoa real, inclusive o seu.

**Nenhum segredo versionado.** O CI dos repositórios de exercício bloqueia credenciais.

---

## Sobre este ser um "ponto de partida com defeitos"

Não é um sistema mal feito por acaso. É um sistema como muitos que existem em produção:
começou funcionando, resolveu o problema imediato, e carrega decisões que ninguém
revisou. A auditoria existe para encontrar essas decisões — as que viraram defeito, as
ambíguas, e as que só cobram depois.

Parte do que você vai encontrar são erros claros. Parte são **ambiguidades de
requisito** que o código resolveu sozinho, sem que ninguém decidisse — e distinguir as
duas coisas é uma das habilidades centrais das duas disciplinas.

---

*Sistema didático © 2026 Petros Barreto. Dados fictícios.*
