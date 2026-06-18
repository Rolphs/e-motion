"""Siembra la base de datos: colores (desde tokens.json) y palabras (seed JSON).

Idempotente: usar INSERT OR IGNORE para poder correrlo varias veces sin duplicar.
Ejecutar:  python -m app.seed
"""

from __future__ import annotations

import json
from pathlib import Path

from app.db import BASE_DIR, get_conn, init_db

TOKENS = BASE_DIR / "assets" / "tokens.json"
SEED_PALABRAS = BASE_DIR / "seed" / "palabras.json"


def _hex_a_rgb(hex_: str) -> str:
    h = hex_.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"{r},{g},{b}"


def sembrar_colores(db: Path | None = None) -> int:
    base = json.loads(TOKENS.read_text(encoding="utf-8"))["palette"]["base"]
    n = 0
    with get_conn(db) as c:
        for orden, (nombre, hex_) in enumerate(base.items()):
            cur = c.execute(
                """INSERT OR IGNORE INTO colores (nombre, hex, rgb, orden)
                   VALUES (?, ?, ?, ?)""",
                (nombre, hex_, _hex_a_rgb(hex_), orden),
            )
            n += cur.rowcount
    return n


def sembrar_palabras(db: Path | None = None) -> int:
    data = json.loads(SEED_PALABRAS.read_text(encoding="utf-8"))["palabras"]
    n = 0
    with get_conn(db) as c:
        for p in data:
            cur = c.execute(
                """INSERT OR IGNORE INTO palabras (termino, definicion, definicion_fuente)
                   VALUES (?, ?, 'manual')""",
                (p["termino"], p["definicion"]),
            )
            n += cur.rowcount
    return n


def sembrar_todo(db: Path | None = None) -> tuple[int, int]:
    init_db(db)
    return sembrar_colores(db), sembrar_palabras(db)


if __name__ == "__main__":
    colores, palabras = sembrar_todo()
    print(f"Sembrado: {colores} colores nuevos, {palabras} palabras nuevas.")
