"""Acceso a datos de Colores: todas las consultas SQL viven aqui (DRY).

Las rutas no tocan SQL directamente; hablan con estas funciones puras-ish.
"""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from app.db import get_conn


def _rows(cur: sqlite3.Cursor) -> list[dict]:
    return [dict(r) for r in cur.fetchall()]


# --- Colores -------------------------------------------------------------

def get_colores(db: Path | None = None) -> list[dict]:
    with get_conn(db) as c:
        return _rows(c.execute("SELECT * FROM colores ORDER BY orden, id"))


def get_color(color_id: int, db: Path | None = None) -> dict | None:
    with get_conn(db) as c:
        r = c.execute("SELECT * FROM colores WHERE id = ?", (color_id,)).fetchone()
        return dict(r) if r else None


# --- Palabras ------------------------------------------------------------

def get_palabras(db: Path | None = None) -> list[dict]:
    with get_conn(db) as c:
        return _rows(
            c.execute(
                "SELECT * FROM palabras WHERE estado = 'activa' ORDER BY termino"
            )
        )


def get_palabra(palabra_id: int, db: Path | None = None) -> dict | None:
    with get_conn(db) as c:
        r = c.execute("SELECT * FROM palabras WHERE id = ?", (palabra_id,)).fetchone()
        return dict(r) if r else None


def contar_palabras(db: Path | None = None) -> int:
    with get_conn(db) as c:
        return c.execute(
            "SELECT COUNT(*) AS n FROM palabras WHERE estado = 'activa'"
        ).fetchone()["n"]


# --- Sesiones ------------------------------------------------------------

def crear_sesion(db: Path | None = None) -> str:
    sid = uuid.uuid4().hex
    with get_conn(db) as c:
        c.execute("INSERT INTO sesiones (id) VALUES (?)", (sid,))
    return sid

def existe_sesion(sesion_id: str, db: Path | None = None) -> bool:
    with get_conn(db) as c:
        return (
            c.execute("SELECT 1 FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
            is not None
        )


def get_sesion(sesion_id: str, db: Path | None = None) -> dict | None:
    with get_conn(db) as c:
        r = c.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
        return dict(r) if r else None


def set_segmento(
    sesion_id: str, genero: str | None, pais: str | None, db: Path | None = None
) -> None:
    with get_conn(db) as c:
        c.execute(
            "UPDATE sesiones SET genero = ?, pais = ? WHERE id = ?",
            (genero or None, pais or None, sesion_id),
        )


# --- Captura -------------------------------------------------------------

def siguiente_palabra(sesion_id: str, db: Path | None = None) -> dict | None:
    """Una palabra que esta sesion aun no haya clasificado (None si termino)."""
    with get_conn(db) as c:
        r = c.execute(
            """
            SELECT p.* FROM palabras p
            WHERE p.estado = 'activa'
              AND p.id NOT IN (
                  SELECT palabra_id FROM asociaciones
                  WHERE sesion_id = ? AND tipo = 'elige'
              )
            ORDER BY RANDOM() LIMIT 1
            """,
            (sesion_id,),
        ).fetchone()
        return dict(r) if r else None


def contar_clasificadas(sesion_id: str, db: Path | None = None) -> int:
    with get_conn(db) as c:
        return c.execute(
            "SELECT COUNT(*) AS n FROM asociaciones WHERE sesion_id = ? AND tipo = 'elige'",
            (sesion_id,),
        ).fetchone()["n"]


def registrar_asociacion(
    sesion_id: str,
    palabra_id: int,
    color_id: int,
    tipo: str = "elige",
    db: Path | None = None,
) -> bool:
    """Guarda la eleccion. Devuelve False si ya existia (doble envio)."""
    try:
        with get_conn(db) as c:
            c.execute(
                """INSERT INTO asociaciones (palabra_id, color_id, sesion_id, tipo)
                   VALUES (?, ?, ?, ?)""",
                (palabra_id, color_id, sesion_id, tipo),
            )
        return True
    except sqlite3.IntegrityError:
        return False


# --- Vistas de lectura (agregaciones) ------------------------------------

def distribucion_por_palabra(palabra_id: int, db: Path | None = None) -> list[dict]:
    """Reparto porcentual de colores para una palabra."""
    with get_conn(db) as c:
        filas = _rows(
            c.execute(
                """
                SELECT col.id, col.nombre, col.hex, COUNT(*) AS n
                FROM asociaciones a
                JOIN colores col ON col.id = a.color_id
                WHERE a.palabra_id = ? AND a.tipo = 'elige'
                GROUP BY col.id ORDER BY n DESC, col.orden
                """,
                (palabra_id,),
            )
        )
    return _con_porcentaje(filas)


def distribucion_por_color(color_id: int, db: Path | None = None) -> list[dict]:
    """Palabras mas asociadas a un color, con su % de match."""
    with get_conn(db) as c:
        filas = _rows(
            c.execute(
                """
                SELECT p.id, p.termino AS nombre, COUNT(*) AS n
                FROM asociaciones a
                JOIN palabras p ON p.id = a.palabra_id
                WHERE a.color_id = ? AND a.tipo = 'elige'
                GROUP BY p.id ORDER BY n DESC, p.termino
                """,
                (color_id,),
            )
        )
    return _con_porcentaje(filas)


def _con_porcentaje(filas: list[dict]) -> list[dict]:
    total = sum(f["n"] for f in filas) or 1
    for f in filas:
        f["pct"] = round(100 * f["n"] / total)
    return filas
