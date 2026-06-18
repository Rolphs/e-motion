"""Colores - aplicacion FastAPI.

Fase 1: bucle de captura (palabra -> color) + vistas de lectura por palabra y
por color. Las rutas son delgadas: la logica de datos vive en app/repo.py.
"""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import repo
from app.db import get_conn, init_db
from app.seed import sembrar_todo
from app.wheel import WHEEL_CX, WHEEL_CY, WHEEL_VIEWBOX, rueda

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

SID_COOKIE = "sid"
META_OBJETIVO = 10  # meta sugerida de palabras por sesion (solo informativo)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with get_conn() as c:
        vacia = c.execute("SELECT COUNT(*) AS n FROM colores").fetchone()["n"] == 0
    if vacia:
        sembrar_todo()
    yield


app = FastAPI(title="Colores", version="0.1.0", lifespan=lifespan)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _sid_actual(request: Request) -> str | None:
    sid = request.cookies.get(SID_COOKIE)
    return sid if sid and repo.existe_sesion(sid) else None


def _set_sid(resp, sid: str) -> None:
    resp.set_cookie(
        SID_COOKIE, sid, httponly=True, samesite="lax", max_age=60 * 60 * 24 * 365
    )


def load_palette() -> list[dict[str, str]]:
    tokens = json.loads((ASSETS_DIR / "tokens.json").read_text(encoding="utf-8"))
    return [{"nombre": n, "hex": h} for n, h in tokens["palette"]["base"].items()]


# --- Salud ---------------------------------------------------------------

@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "app": "colores", "version": app.version})


# --- Landing -------------------------------------------------------------

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request, "index.html", {"palette": load_palette()}
    )


# --- Segmentacion (opcional) ---------------------------------------------

@app.get("/segmento")
def segmento_form(request: Request):
    return templates.TemplateResponse(request, "segmento.html", {})


@app.post("/segmento")
def segmento_guardar(
    request: Request,
    genero: str = Form(default=""),
    pais: str = Form(default=""),
):
    resp = RedirectResponse("/clasificar", status_code=303)
    sid = _sid_actual(request)
    if sid is None:
        sid = repo.crear_sesion()
        _set_sid(resp, sid)
    repo.set_segmento(sid, genero, pais)
    return resp


# --- Bucle de captura ----------------------------------------------------

def _ctx_captura(sid: str) -> dict:
    return {
        "palabra": repo.siguiente_palabra(sid),
        "rueda": rueda(repo.get_colores()),
        "wheel_viewbox": WHEEL_VIEWBOX,
        "wheel_cx": WHEEL_CX,
        "wheel_cy": WHEEL_CY,
        "n": repo.contar_clasificadas(sid),
        "total": repo.contar_palabras(),
        "meta": META_OBJETIVO,
    }


@app.get("/clasificar")
def clasificar(request: Request):
    sid = _sid_actual(request)
    nuevo = sid is None
    if nuevo:
        sid = repo.crear_sesion()
    resp = templates.TemplateResponse(request, "clasificar.html", _ctx_captura(sid))
    if nuevo:
        _set_sid(resp, sid)
    return resp


@app.post("/clasificar")
def clasificar_guardar(
    request: Request,
    palabra_id: int = Form(...),
    color_id: int = Form(...),
):
    sid = _sid_actual(request)
    if sid is None:
        # Sin sesion valida: pedimos recargar la pagina completa.
        return HTMLResponse(
            '<div id="card" hx-get="/clasificar" hx-trigger="load"></div>'
        )
    repo.registrar_asociacion(sid, palabra_id, color_id)  # ignora doble envio
    return templates.TemplateResponse(
        request, "partials/_card.html", _ctx_captura(sid)
    )


# --- Vistas de lectura (lexicon) -----------------------------------------

@app.get("/lexico")
def lexico(request: Request):
    return templates.TemplateResponse(
        request,
        "lexico.html",
        {"palabras": repo.get_palabras(), "colores": repo.get_colores()},
    )


@app.get("/lexico/palabra/{palabra_id}")
def lexico_palabra(request: Request, palabra_id: int):
    palabra = repo.get_palabra(palabra_id)
    if palabra is None:
        return RedirectResponse("/lexico", status_code=303)
    return templates.TemplateResponse(
        request,
        "lexico_palabra.html",
        {"palabra": palabra, "dist": repo.distribucion_por_palabra(palabra_id)},
    )


@app.get("/lexico/color/{color_id}")
def lexico_color(request: Request, color_id: int):
    color = repo.get_color(color_id)
    if color is None:
        return RedirectResponse("/lexico", status_code=303)
    return templates.TemplateResponse(
        request,
        "lexico_color.html",
        {"color": color, "dist": repo.distribucion_por_color(color_id)},
    )
