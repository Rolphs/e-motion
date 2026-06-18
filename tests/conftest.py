"""Configuracion de pytest: usa una BD temporal para no tocar datos reales.

Debe correr ANTES de importar app.db / app.main (conftest se importa primero).
"""

import os
import tempfile
from pathlib import Path

_TMP = Path(tempfile.gettempdir()) / "colores_test.db"
if _TMP.exists():
    _TMP.unlink()
os.environ["COLORES_DB"] = str(_TMP)
