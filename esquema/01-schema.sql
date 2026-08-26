-- Esquema do acervo da Biblioteca Municipal (SQLite).
-- Sistema de laboratorio. As decisoes deste esquema fazem parte do que a
-- auditoria deve avaliar.

DROP TABLE IF EXISTS emprestimo;
DROP TABLE IF EXISTS exemplar;
DROP TABLE IF EXISTS titulo;
DROP TABLE IF EXISTS leitor;

CREATE TABLE titulo (
  titulo_id   INTEGER PRIMARY KEY,
  nome        TEXT    NOT NULL,
  autor       TEXT    NOT NULL,
  isbn        TEXT
);

CREATE TABLE exemplar (
  codigo      TEXT    PRIMARY KEY,
  titulo_id   INTEGER NOT NULL REFERENCES titulo(titulo_id),
  situacao    TEXT    NOT NULL
);

CREATE TABLE leitor (
  leitor_id   INTEGER PRIMARY KEY,
  nome        TEXT    NOT NULL,
  telefone    TEXT,
  categoria   TEXT    NOT NULL
);

CREATE TABLE emprestimo (
  emprestimo_id    INTEGER PRIMARY KEY,
  codigo_exemplar  TEXT    NOT NULL,
  leitor_id        INTEGER NOT NULL REFERENCES leitor(leitor_id) ON DELETE CASCADE,
  categoria        TEXT    NOT NULL,
  leitor_nome      TEXT,
  leitor_telefone  TEXT,
  data_emprestimo  TEXT    NOT NULL,
  data_prevista    TEXT    NOT NULL,
  data_devolucao   TEXT,
  multa            REAL    DEFAULT 0.0
);
