# Colores

> Un lexicón colaborativo que traduce entre **colores, palabras y emociones** — la capa de captura de datos para un sistema de hiperpersonalización de experiencias basado en ML/AI.

Colores forma parte de **emotion**.

---

## Visión

Colores no es un fin en sí mismo: es la **capa de captura de datos** de una iniciativa más amplia de **hiperpersonalización**. El objetivo de fondo es entender cómo distintas personas asocian **conceptos** (palabras) con **emociones y sensaciones**, usando el **color** como vehículo medible.

Una vez aprendidas esas asociaciones por segmento, se pueden invertir: en lugar de solo *describir* cómo siente la gente, se podrán *generar* experiencias de uso que resuenen emocionalmente con cada perfil. La meta a futuro es que **diferentes segmentos de personas tengan experiencias de uso diferentes**, afinadas a su huella emocional-sensorial.

El color es el punto de partida lógico porque es la dimensión sensorial más fácil de cuantificar y de etiquetar sin fricción. El mismo método podría extenderse después a otras modalidades (sonido, forma, textura, ritmo).

## El concepto

> *"Una paleta de colores para expresar diferentes sentimientos, emociones e ideas."*

En esencia, Colores es una base de datos viva de asociaciones **color ↔ significado**, alimentada por las personas, que luego sirve tanto para **analizar** (la huella emocional de un texto o imagen) como para **diseñar y personalizar** experiencias. La biblioteca consultable del proyecto se llama **Lexicon**.

## El problema y la oportunidad

**El problema:** no existe un consenso documentado sobre qué color significa qué. Diseñadores, marcas y artistas eligen color por intuición o tendencia, sin evidencia de qué siente la gente; las asociaciones color↔emoción varían por género, edad y país, y nadie las tiene cuantificadas; y no hay forma de auditar si una paleta "dice" lo que pretende decir.

**La oportunidad:** un *crowdsourcing* estructurado —un test corto y adictivo— genera datos limpios a escala y produce un activo único, el léxico, que ninguna herramienta de color posee hoy. Es aplicable a branding, marketing, arte, investigación y accesibilidad.

## Cómo funciona

La experiencia se plantea como un recorrido interactivo donde, cada 3 a 5 saltos de página, aparece un **test** breve: el usuario elige qué color asocia con una palabra (p. ej. *Felicidad*, *Cálido*, *Deporte*, *Decadente*) o decide cuál le hace más y menos sentido. Resolver el reto es requisito antes de ver información, de modo que el sistema captura datos de asociación de forma continua.

Cada palabra se ancla a su **definición formal** (DRAE), dando un soporte semántico al ejercicio emocional.

## Los datos que genera

El sistema cuantifica las asociaciones en dos direcciones:

- **Por palabra** — para un término como *Felicidad*: los colores más asociados y su reparto porcentual (50/30/10/7/3%), con conceptos satélite (Sol, Energía, Tranquilidad, Suerte, Luz).
- **Por color** — para un color como *Azul*: ficha técnica completa (RGB / CMYK / HEX), número de entradas, ranking de preferencia por género y país, y palabras asociadas con su % de match (Tranquilo 90%, Confianza 10%, Libertad 3%, Frío 1%…).

La segmentación (género, país y, a futuro, más variables) es central: las asociaciones **no son universales**, varían por cultura, edad y contexto. Capturar esa variación es lo que habilita la hiperpersonalización.

## Funciones del producto

Desde el menú *"¿Qué quieres hacer?"*:

- **Calibrar colores** — ajustar/afinar las asociaciones.
- **Clasificar / aportar palabras** — hacer crecer el lexicón con nuevos términos.
- **Biblioteca de colores (lexicón)** — consultar el diccionario de asociaciones.
- **Análisis de texto** — obtener la paleta emocional de un texto.
- **Análisis de imagen** — obtener la paleta emocional de una imagen.

Análisis de texto e imagen son la aplicación práctica directa: a partir de un input, el sistema devuelve qué colores —y por tanto qué emociones— predominan, con su desglose porcentual.

## El lexicón

Es el corazón del sistema: un diccionario A–Z de palabras (Alegría, Alto, Adicional…) que conecta cada término con colores y emociones, y que crece con las aportaciones de los usuarios ("palabras que no aparecen en nuestro lexicón").

## El arco completo

1. **Capturar** asociaciones emoción ↔ concepto, mediadas por color (Colores).
2. **Entrenar** modelos de ML/AI que aprendan los patrones por segmento.
3. **Hiperpersonalizar** experiencias: dos personas distintas viven versiones distintas, afinadas a su perfil emocional-sensorial.

## Casos de uso y mercado

- **Branding y marketing** — validar que una paleta transmite la emoción correcta, con evidencia y por segmento.
- **Diseño y producto** — elegir color con datos en vez de intuición; auditar interfaces y campañas.
- **Arte e investigación** — material de estudio sobre percepción del color por cultura, género y edad.
- **Educación y curiosidad** — una experiencia lúdica que enseña sobre uno mismo mientras alimenta el léxico.

## Modelo de negocio *(propuesta)*

El deck no define monetización; estas son rutas coherentes con el producto. El activo defendible es el léxico: cuanta más gente clasifica, más valioso es el dato.

- **Freemium** — clasificar es gratis y adictivo; registrarse desbloquea las herramientas de análisis y la biblioteca completa.
- **Soportado por publicidad** — un nivel gratuito con anuncios financia el acceso abierto.
- **API / licencia de datos** — marcas y herramientas de diseño consultan el léxico vía API (el caso comercial de mayor valor).
- **Análisis premium** — informes de texto e imagen a fondo para equipos de marketing, branding e investigación.

## Roadmap *(propuesta)*

1. **Semilla del léxico** — definir el set base de 2 500 palabras y la mecánica de clasificación; lanzar el bucle *definir → elegir → agregar*.
2. **Data y calibración** — vistas por palabra y por color, test recurrente, segmentación por género, edad y país.
3. **Herramientas de análisis** — análisis de texto e imagen, biblioteca Lexicon navegable, cuentas registradas.
4. **Plataforma y API** — apertura del léxico vía API, monetización (premium + datos) y expansión a más idiomas y culturas.

## Identidad visual

Tokens disponibles en [`assets/tokens.json`](assets/tokens.json) y [`assets/tokens.css`](assets/tokens.css).

**Paleta base**

| Color | HEX | Color | HEX |
|---|---|---|---|
| Amarillo | `#F9E547` | Morado | `#9437FF` |
| Naranja | `#FF9300` | Café | `#945200` |
| Rojo | `#FF0000` | Negro | `#000000` |
| Azul | `#0077C8` | Gris | `#D6D6D6` |
| Verde | `#008F00` | Blanco | `#F5FAFF` |

**Colores de marca:** Tinta `#28282D` · Azul primario `#0071BC` · Acento `#FF4600`

**Tipografías:** Raleway SemiBold (títulos) · Raleway Light (objetos y botones) · Quattrocento (textos) · Raleway Dots (notas).

## Documentación

- [`docs/Colores-documento-proyecto.html`](docs/Colores-documento-proyecto.html) — documento del proyecto completo (11 secciones).
- [`docs/Colores-deck.pptx`](docs/Colores-deck.pptx) — deck conceptual original (13 láminas).
- [`docs/detallada/`](docs/detallada/) — espejo **interactivo** del documento del proyecto (`*.interactivo.html` + `support.js`), exportado con navegador embebido. Mismo contenido que el HTML plano, con UI navegable.

## Activos existentes

El proyecto cuenta con materiales ya desarrollados (mayo 2021 – nov 2022), ubicados en
`OneDrive-Personal/emotion/Colores/`:

- `Colores.key` / `Colores.pptx` — deck conceptual (13 láminas).
- `Colores.ai` — objetos editables en Illustrator.
- `Recursos/` — ~19 SVGs (íconos: croma, calibrar, clasificar, foco, gráficas, información, pulgar arriba/abajo…), mapa, fuentes y plantillas de Keynote.

## Estado

Fase de **conceptualización / definición de alcance**. Próximos pasos candidatos: traer los activos al repo, definir el modelo de datos del lexicón (esquema color ↔ palabra ↔ segmento) y prototipar el flujo de captura.
