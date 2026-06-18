"""Tests de la rueda cromatica: orden aleatorio con separacion perceptual."""

import random

from app.wheel import delta_e, hex_a_lab, rueda

# Paleta base del proyecto (incluye los pares "parecidos": blanco/gris, naranja/cafe).
PALETA = [
    {"nombre": "amarillo", "hex": "#F9E547"},
    {"nombre": "naranja", "hex": "#FF9300"},
    {"nombre": "rojo", "hex": "#FF0000"},
    {"nombre": "azul", "hex": "#0077C8"},
    {"nombre": "verde", "hex": "#008F00"},
    {"nombre": "morado", "hex": "#9437FF"},
    {"nombre": "cafe", "hex": "#945200"},
    {"nombre": "negro", "hex": "#000000"},
    {"nombre": "gris", "hex": "#D6D6D6"},
    {"nombre": "blanco", "hex": "#F5FAFF"},
]


def _min_adyacente(orden: list[dict]) -> float:
    labs = [hex_a_lab(c["hex"]) for c in orden]
    n = len(labs)
    return min(delta_e(labs[i], labs[(i + 1) % n]) for i in range(n))


def test_pares_parecidos_nunca_adyacentes():
    """En muchas corridas, blanco/gris y naranja/cafe nunca son vecinos."""
    prohibidos = {("blanco", "gris"), ("cafe", "naranja")}
    for _ in range(300):
        r = rueda(PALETA, random.Random())
        n = len(r)
        adyacentes = {
            tuple(sorted((r[i]["nombre"], r[(i + 1) % n]["nombre"]))) for i in range(n)
        }
        assert not (prohibidos & adyacentes)


def test_separacion_minima_se_respeta():
    """La minima distancia adyacente supera holgadamente al par mas parecido."""
    for _ in range(300):
        assert _min_adyacente(rueda(PALETA, random.Random())) > 12.8


def test_es_aleatorio():
    """Dos semillas distintas producen, casi siempre, ordenes distintos."""
    a = [c["nombre"] for c in rueda(PALETA, random.Random(1))]
    b = [c["nombre"] for c in rueda(PALETA, random.Random(2))]
    assert a != b


def test_conserva_todos_los_colores():
    r = rueda(PALETA, random.Random(0))
    assert sorted(c["nombre"] for c in r) == sorted(c["nombre"] for c in PALETA)
