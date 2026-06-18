"""Rueda cromatica: lee los 10 segmentos SVG originales del proyecto.

Los archivos assets/icons/Colores_01.svg .. Colores_10.svg son cada uno un
"petalo" de la rueda (Colores_Croma.svg), todos en el mismo sistema de
coordenadas. Aqui extraemos su path para tintarlos y hacerlos clickeables,
manteniendo el arte original como fuente unica de verdad (DRY).
"""

from __future__ import annotations

import re
from functools import lru_cache

from app.db import BASE_DIR

ICONS_DIR = BASE_DIR / "assets" / "icons"

# viewBox cuadrado centrado en el centro de la rueda (de Colores_Croma.svg),
# para que el anillo salga circular (no estirado) y la palabra caiga en el hueco.
WHEEL_VIEWBOX = "44 160 520 520"
WHEEL_CX = 304
WHEEL_CY = 420

_D_RE = re.compile(r'\sd="([^"]+)"')


@lru_cache(maxsize=1)
def cargar_segmentos() -> list[str]:
    """Path 'd' de cada segmento, en orden 01..10 (cacheado)."""
    paths: list[str] = []
    for i in range(1, 11):
        svg = (ICONS_DIR / f"Colores_{i:02d}.svg").read_text(encoding="utf-8")
        m = _D_RE.search(svg)
        if m:
            paths.append(m.group(1))
    return paths


def rueda(colores: list[dict]) -> list[dict]:
    """Empareja cada color (por orden) con su segmento de la rueda."""
    segs = cargar_segmentos()
    salida = []
    for idx, color in enumerate(colores):
        if idx < len(segs):
            salida.append({**color, "d": segs[idx]})
    return salida
