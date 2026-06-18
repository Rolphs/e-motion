"""Tests de Fase 1: capa de datos (repo) + flujo de captura via HTTP."""

import re

from fastapi.testclient import TestClient

from app import repo
from app.main import app
from app.seed import sembrar_todo


def test_seed_idempotente_y_repo(tmp_path):
    db = tmp_path / "t.db"
    colores, palabras = sembrar_todo(db)
    assert colores == 10
    assert palabras == 25
    # correr de nuevo no duplica
    assert sembrar_todo(db) == (0, 0)
    assert len(repo.get_colores(db)) == 10
    assert repo.contar_palabras(db) == 25


def test_asociacion_y_distribucion(tmp_path):
    db = tmp_path / "t.db"
    sembrar_todo(db)
    sid = repo.crear_sesion(db)
    palabra = repo.siguiente_palabra(sid, db)
    color = repo.get_colores(db)[0]

    assert repo.registrar_asociacion(sid, palabra["id"], color["id"], db=db) is True
    # doble envio: la misma sesion no cuenta dos veces la misma palabra
    assert repo.registrar_asociacion(sid, palabra["id"], color["id"], db=db) is False
    assert repo.contar_clasificadas(sid, db) == 1

    dist = repo.distribucion_por_palabra(palabra["id"], db)
    assert dist[0]["nombre"] == color["nombre"]
    assert dist[0]["pct"] == 100


def test_siguiente_palabra_se_agota(tmp_path):
    db = tmp_path / "t.db"
    sembrar_todo(db)
    sid = repo.crear_sesion(db)
    vistas = set()
    while (p := repo.siguiente_palabra(sid, db)) is not None:
        assert p["id"] not in vistas
        vistas.add(p["id"])
        repo.registrar_asociacion(sid, p["id"], repo.get_colores(db)[0]["id"], db=db)
    assert len(vistas) == 25
    assert repo.siguiente_palabra(sid, db) is None


def test_segmento_opcional(tmp_path):
    db = tmp_path / "t.db"
    sembrar_todo(db)
    sid = repo.crear_sesion(db)
    repo.set_segmento(sid, "mujer", "Mexico", db)
    s = repo.get_sesion(sid, db)
    assert s["genero"] == "mujer"
    assert s["pais"] == "Mexico"


def test_flujo_captura_http():
    with TestClient(app) as client:
        # health
        assert client.get("/health").json()["status"] == "ok"

        # landing y lexico cargan
        assert client.get("/").status_code == 200
        assert client.get("/lexico").status_code == 200

        # primera tarjeta de captura (rueda cromatica)
        r = client.get("/clasificar")
        assert r.status_code == 200
        assert client.cookies.get("sid")
        assert 'class="wheel__svg"' in r.text
        m = re.search(r'"palabra_id": (\d+), "color_id": (\d+)', r.text)
        palabra_id, color_id = m.group(1), m.group(2)

        # POST de una eleccion -> devuelve la siguiente tarjeta (partial)
        r2 = client.post(
            "/clasificar", data={"palabra_id": palabra_id, "color_id": color_id}
        )
        assert r2.status_code == 200
        assert 'id="card"' in r2.text

        # la vista por palabra ya refleja la eleccion
        r3 = client.get(f"/lexico/palabra/{palabra_id}")
        assert r3.status_code == 200
        assert "100%" in r3.text
