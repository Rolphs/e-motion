# Inventario de activos

Activos del proyecto Colores importados desde `OneDrive/EIDOS/emotion/Colores` (origen: mayo 2021 – nov 2022). Solo se conservó lo que aporta valor; el ruido quedó fuera (ver más abajo).

## Estructura

```
docs/      → Colores-deck.pptx     deck conceptual (13 láminas)
design/
  source/  → Colores.ai, mapa.ai   fuentes editables (Illustrator)
assets/
  icons/   → Colores_*.svg (19)    iconografía del producto
  fonts/   → *.ttf (5)             tipografías de marca
  map/     → mapa.svg              mapa/flujo del proyecto
```

## Íconos del producto (`assets/icons/`)

Iconografía funcional, alineada al menú de la app:

- **Funciones**: `calibrar`, `clasificar`, `graficas`, `informacion`, `foco`, `acomodar`, `Croma`
- **Feedback**: `pulgar arriba`, `pulgar abajo`
- **Set numerado**: `Colores_01` … `Colores_10`

## Tipografías de marca (`assets/fonts/`)

- **Raleway** (Light / SemiBold / Thin) — títulos y objetos
- **Quattrocento** — textos
- **Raleway Dots** — notas

## Fuentes editables (`design/source/`)

- `Colores.ai` — objetos e iconografía originales
- `mapa.ai` — fuente editable del mapa

## Descartado (no aportaba valor)

- `IMG_1974.png` — foto suelta (12 MB), sin relación con el sistema.
- `Recursos/keynote/` — internos de plantillas Keynote (`tile_paper`, `White_photo`, `.apxl`, `.ezdraw`) y mockups de tazas de café.
- `Recursos/otros recursos/noun_*` — íconos de stock (café/tazas/té) de un contexto ajeno.
- `mapa-01.svg`, `mapaMesa de trabajo 1.svg`, `mapaRecurso 1.svg` — duplicados/variantes de `mapa.svg`.
- `Colores.zip` — archivo redundante.
- `Colores.key` — equivalente al `.pptx` (formato Keynote, menos portable para versionar). El `.pptx` conserva el mismo contenido.
