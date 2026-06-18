"""Smoke tests de la Fase 0: la app arranca y sirve lo basico."""

from fastapi.testclient import TestClient

from app.main import app, load_palette

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_index_renderiza_paleta():
    r = client.get("/")
    assert r.status_code == 200
    assert "Colores" in r.text
    # los 10 colores de la paleta base deben aparecer
    for color in load_palette():
        assert color["hex"] in r.text


def test_palette_desde_tokens():
    palette = load_palette()
    assert len(palette) == 10
    assert {"nombre": "azul", "hex": "#0077C8"} in palette
