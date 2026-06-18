# Roadmap — Colores

> Documento **indicativo, no contractual**. Marca el rumbo y el orden sugerido;
> las prioridades pueden moverse según lo que aprendamos. Vive y se actualiza
> con el proyecto. Para el "qué" y el "por qué" del producto, ver [`README.md`](README.md).

**Estado actual:** fase de conceptualización. Existen identidad visual, design
tokens (`assets/tokens.{css,json}`), iconografía, fuentes y documentación. **Aún
no hay código de aplicación ni una sola asociación capturada.**

**Principio rector:** Colores es la *capa de captura de datos*. El activo
defendible es el léxico. Por tanto, **primero capturamos, luego analizamos**.
Construir el análisis con ML antes de tener datos sería techo sin cimientos
(YAGNI). El orden de las fases respeta esa dependencia.

---

## Decisiones ya tomadas

| Tema | Decisión | Nota |
|---|---|---|
| Stack | Python + FastAPI + HTMX + Tailwind + SQLite | Default del workspace; sin SPA hasta que duela. |
| Segmentación | Anónimo + **género/país opcionales** | Pantalla rápida opcional al entrar; fricción mínima, dato segmentable. |
| Definiciones | Anclar cada palabra a su definición (DRAE) | Estrategia y riesgos en la sección "Definiciones (DRAE)" más abajo. |
| Accesibilidad | WCAG 2.2 AA + consideración daltonismo | Trabajamos *con color*: el color nunca puede ser el único portador de significado. |
| Hosting (a futuro) | AI Innovation Lab | Para webapp pública; ver fase 4. |

---

## Fase 0 — Fundamentos *(hecho)*

- [x] Importar y ordenar activos (assets, design, docs) en el repo.
- [x] Design tokens en CSS + JSON.
- [x] `git init` + `.gitignore`.
- [x] Esqueleto del proyecto FastAPI (estructura `app/`, `pyproject.toml`, venv con `uv`).
- [x] Página base que carga fuentes y tokens reales (smoke test visual + 3 tests verdes).

## Fase 1 — Semilla del léxico + bucle de captura *(MVP — el corazón)*

El objetivo: una app **usable y desplegable que ya captura datos reales**.

- [ ] **Modelo de datos** (ver esquema abajo): `palabras`, `colores`,
      `asociaciones`, `segmentos`/`sesiones`.
- [ ] **Seed de colores**: los 10 de la paleta base (ya en tokens).
- [ ] **Seed de palabras**: empezar pequeño (~20-30), no las 2.500 de golpe.
- [ ] **Definiciones**: resolver la estrategia DRAE para el seed inicial.
- [ ] **Bucle de captura** (HTMX): palabra + definición → 10 colores como
      botones accesibles → guardar elección → siguiente palabra, sin recargar.
- [ ] **Segmentación opcional**: pantalla inicial (género/país) que se puede saltar;
      se guarda en la sesión y se adjunta a cada asociación.
- [ ] **Dos vistas de lectura mínimas**:
  - *Por palabra*: reparto porcentual de colores asociados.
  - *Por color*: palabras más asociadas y su % de match.
- [ ] **Anti-ruido básico**: rate-limit por sesión, evitar doble envío.

**Criterio de "terminado":** un desconocido puede entrar, clasificar 10 palabras
y ver cómo cambian las dos vistas. Datos persistidos en SQLite.

## Fase 2 — Data y calibración

- [ ] **Calibrar colores**: mecánica para afinar/confirmar asociaciones existentes.
- [ ] **Clasificar / aportar palabras**: que los usuarios propongan términos nuevos
      ("palabras que no están en el lexicón") → cola de moderación.
- [ ] **Test recurrente**: el reto reaparece cada 3-5 vistas (mecánica adictiva del README).
- [ ] **Analítica de segmentación**: cortes por género/país; detectar diferencias.
- [ ] **Ficha de color completa**: RGB / CMYK / HEX, nº de entradas, ranking por segmento.
- [ ] **Conceptos satélite** por palabra (p. ej. Felicidad → Sol, Energía, Suerte).

## Fase 3 — Herramientas de análisis

- [ ] **Biblioteca Lexicon** navegable A–Z (el diccionario consultable).
- [ ] **Cuentas registradas** (desbloquean herramientas; freemium del README).
- [ ] **Análisis de texto**: input de texto → paleta emocional con desglose %.
- [ ] **Análisis de imagen**: input de imagen → paleta emocional con desglose %.
  - *Aquí entra el primer ML real, ya con dataset propio que lo justifique.*

## Fase 4 — Plataforma y API

- [ ] **API del léxico** (el caso comercial de mayor valor según el README).
- [ ] **Monetización**: premium + licencia de datos.
- [ ] **i18n**: expansión a más idiomas y culturas (la segmentación lo exige).
- [ ] **Despliegue público** vía AI Innovation Lab (https://wmlink.wal-mart.com/onboard).

---

## Esquema de datos propuesto *(borrador, fase 1)*

```text
colores
  id            INTEGER PK
  nombre        TEXT      -- "azul"
  hex           TEXT      -- "#0077C8"
  rgb           TEXT      -- "0,119,200"
  orden         INTEGER   -- para UI

palabras
  id            INTEGER PK
  termino       TEXT UNIQUE
  definicion    TEXT      -- texto DRAE (o NULL si pendiente)
  definicion_fuente TEXT  -- "drae" | "manual" | "wiktionary" | NULL
  estado        TEXT      -- "activa" | "propuesta" | "rechazada"
  creada_en     TIMESTAMP

sesiones                  -- usuario anónimo
  id            TEXT PK   -- uuid en cookie
  genero        TEXT      -- opcional, NULL permitido
  pais          TEXT      -- opcional, NULL permitido
  creada_en     TIMESTAMP

asociaciones              -- el dato de oro
  id            INTEGER PK
  palabra_id    INTEGER FK -> palabras
  color_id      INTEGER FK -> colores
  sesion_id     TEXT FK    -> sesiones
  tipo          TEXT       -- "elige" | "descarta" (el "más / menos sentido")
  creada_en     TIMESTAMP
```

> Las vistas "por palabra" y "por color" son agregaciones (`GROUP BY`) sobre
> `asociaciones`. Nada de tablas de cache prematuras (YAGNI) hasta que el volumen
> lo pida.

---

## Definiciones (DRAE) — riesgo a resolver en fase 1

Honestidad ante todo: **el DRAE no ofrece API oficial pública.** Opciones, de
menos a más fricción:

1. **Seed manual** para el primer puñado de palabras — cero dependencias, arranca ya.
2. **Wiktionary / Wikcionario API** — abierta y legal, formato distinto al DRAE
   pero perfectamente válido como "definición formal". *Candidata preferida.*
3. **Wrappers comunitarios del DRAE** (no oficiales) — frágiles, pueden romperse
   y quedan en una zona gris de términos de uso. Usar con cautela.
4. **Scraping directo de rae.es** — desaconsejado: frágil y legalmente turbio.

**Plan sugerido:** arrancar con (1) para no bloquearnos, y evaluar (2) como
fuente automática estable. Decidir antes de cerrar fase 1.

---

## Temas transversales (aplican a todas las fases)

- **Accesibilidad del color:** etiquetar siempre el color con su nombre (texto),
  no solo el swatch. Cumplir contraste WCAG 2.2 AA. Pensar en daltonismo.
- **Privacidad:** género/país son datos personales aunque sean opcionales y
  anónimos. Nada de PII en git; agregados, no perfiles individuales.
- **Calidad del dato:** anti-bot/anti-ruido desde fase 1 (el léxico vale por su
  limpieza). 
- **Tests:** por feature, aislados. E2E con Playwright cuando haya UI estable.
- **Commits frecuentes:** rodar adelante y atrás con git (Zen + reglas del workspace).

---

## Siguiente paso concreto sugerido

Cerrar **Fase 0**: montar el esqueleto FastAPI (`uv venv`, estructura de
carpetas, página base con tokens y fuentes reales) y de ahí saltar al modelo de
datos de Fase 1. Pequeño, verificable, desplegable.
