"""Colores - aplicacion FastAPI (Fase 0: esqueleto + smoke test visual).

Sirve una pagina base que carga las fuentes y los design tokens reales del
proyecto, y expone los colores de la paleta leyendolos de `assets/tokens.json`
(fuente unica de verdad). Sin logica de negocio todavia.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Colores", version="0.0.1")

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def load_palette() -> list[dict[str, str]]:
    """Lee la paleta base desde assets/tokens.json (fuente unica de verdad)."""
    tokens = json.loads((ASSETS_DIR / "tokens.json").read_text(encoding="utf-8"))
    base = tokens["palette"]["base"]
    return [{"nombre": nombre, "hex": hex_} for nombre, hex_ in base.items()]


@app.get("/health")
def health() -> JSONResponse:
    """Liveness check."""
    return JSONResponse({"status": "ok", "app": "colores", "version": app.version})


@app.get("/")
def index(request: Request):
    """Smoke test visual: fuentes + tokens + paleta renderizada."""
    return templates.TemplateResponse(
        request,
        "index.html",
        {"palette": load_palette()},
    )
