"""Rueda cromatica: lee los 10 segmentos SVG originales del proyecto.

Los archivos assets/icons/Colores_01.svg .. Colores_10.svg son cada uno un
"petalo" de la rueda (Colores_Croma.svg), todos en el mismo sistema de
coordenadas. Aqui extraemos su path para tintarlos y hacerlos clickeables,
manteniendo el arte original como fuente unica de verdad (DRY).
"""

from __future__ import annotations

import random
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


def _srgb_a_lineal(canal: int) -> float:
    """Quita la correccion gamma de un canal sRGB (0..255) -> lineal (0..1)."""
    c = canal / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_a_lab(hex_color: str) -> tuple[float, float, float]:
    """Convierte '#RRGGBB' a CIELAB (L*, a*, b*) bajo iluminante D65.

    Trabajamos en un espacio *perceptual*: distancias iguales en Lab se
    perciben como diferencias de color similares. Asi, "parecido" deja de
    ser una lista de pares a mano y pasa a ser una magnitud medible (DeltaE).
    """
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    rl, gl, bl = _srgb_a_lineal(r), _srgb_a_lineal(g), _srgb_a_lineal(b)
    # sRGB lineal -> XYZ (matriz estandar D65)
    x = rl * 0.4124 + gl * 0.3576 + bl * 0.1805
    y = rl * 0.2126 + gl * 0.7152 + bl * 0.0722
    z = rl * 0.0193 + gl * 0.1192 + bl * 0.9505
    # XYZ -> Lab (normalizado al blanco de referencia D65)
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(c1: tuple[float, float, float], c2: tuple[float, float, float]) -> float:
    """Distancia perceptual entre dos colores en Lab (DeltaE CIE76)."""
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2) ** 0.5


def _orden_separado(
    colores: list[dict], rng: random.Random, intentos: int = 400
) -> list[dict]:
    """Orden aleatorio con separacion perceptual minima entre vecinos (ciclico).

    Rejection sampling con umbral autocalibrado: empezamos exigiendo que cada
    par adyacente (incluido ultimo<->primero, porque la rueda es un anillo)
    supere la *mediana* de todas las distancias por pares, y relajamos el
    umbral si esa exigencia resulta infactible. No hay pares ni constantes
    hardcodeadas: el umbral se deriva de la propia paleta.
    """
    n = len(colores)
    if n < 3:
        rng.shuffle(colores)
        return colores

    labs = [hex_a_lab(c["hex"]) for c in colores]
    dist = [[delta_e(labs[i], labs[j]) for j in range(n)] for i in range(n)]
    pares = sorted(dist[i][j] for i in range(n) for j in range(i + 1, n))
    umbral = pares[len(pares) // 2]  # mediana -> calibrado a la paleta

    idx = list(range(n))
    while umbral > 1e-6:
        for _ in range(intentos):
            rng.shuffle(idx)
            minimo = min(dist[idx[k]][idx[(k + 1) % n]] for k in range(n))
            if minimo >= umbral:
                return [colores[i] for i in idx]
        umbral *= 0.9  # nadie cumplio: aflojamos y reintentamos
    rng.shuffle(colores)  # paleta degenerada (colores casi identicos)
    return colores


def rueda(colores: list[dict], rng: random.Random | None = None) -> list[dict]:
    """Empareja cada color con un segmento de la rueda.

    Los colores se ordenan al azar en cada llamada (para que aparezcan en
    distinto orden), pero respetando una separacion perceptual minima: dos
    colores muy parecidos (p. ej. gris y blanco) nunca quedan adyacentes.
    La figura de la rueda no cambia: los segmentos son siempre los mismos,
    solo cambia que color ocupa cada uno.

    `rng` permite inyectar un generador con semilla (util en tests).
    """
    rng = rng or random
    segs = cargar_segmentos()
    colores = _orden_separado(list(colores), rng)
    salida = []
    for idx, color in enumerate(colores):
        if idx < len(segs):
            salida.append({**color, "d": segs[idx]})
    return salida
