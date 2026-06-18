"""Capa de base de datos (SQLite stdlib) para Colores.

Sin ORM a proposito: a este tamano sqlite3 + SQL crudo es mas simple y
transparente (YAGNI). Aqui viven la conexion, el esquema y su inicializacion.
"""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
# Permite apuntar a otra BD (p. ej. tests) via COLORES_DB.
DB_PATH = Path(os.environ.get("COLORES_DB") or (DATA_DIR / "colores.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS colores (
    id      INTEGER PRIMARY KEY,
    nombre  TEXT NOT NULL UNIQUE,
    hex     TEXT NOT NULL,
    rgb     TEXT,
    orden   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS palabras (
    id                INTEGER PRIMARY KEY,
    termino           TEXT NOT NULL UNIQUE,
    definicion        TEXT,
    definicion_fuente TEXT,
    estado            TEXT NOT NULL DEFAULT 'activa',
    creada_en         TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sesiones (
    id        TEXT PRIMARY KEY,
    genero    TEXT,
    pais      TEXT,
    creada_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS asociaciones (
    id         INTEGER PRIMARY KEY,
    palabra_id INTEGER NOT NULL REFERENCES palabras(id),
    color_id   INTEGER NOT NULL REFERENCES colores(id),
    sesion_id  TEXT NOT NULL REFERENCES sesiones(id),
    tipo       TEXT NOT NULL DEFAULT 'elige',
    creada_en  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Una sesion clasifica cada palabra una sola vez (evita doble envio / ruido).
CREATE UNIQUE INDEX IF NOT EXISTS idx_asoc_unica
    ON asociaciones (sesion_id, palabra_id, tipo);
"""


def get_db_path() -> Path:
    return DB_PATH


@contextmanager
def get_conn(db_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Conexion con row factory de dict y claves foraneas activas."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: Path | None = None) -> None:
    """Crea las tablas si no existen (idempotente)."""
    with get_conn(db_path) as conn:
        conn.executescript(SCHEMA)
