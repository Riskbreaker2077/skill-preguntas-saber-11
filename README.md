<div align="center">

# skill-preguntas-saber-11

**Skill de Claude Code que escribe preguntas tipo ICFES Saber 11.° a partir de la documentación oficial y las entrega como paquete ZIP validado.**

[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-blue.svg)](LICENSE)
[![Formato](https://img.shields.io/badge/formato-preguntas--icfes%20v1.4.0-6e40c9.svg)](https://github.com/Riskbreaker2077/preguntas-icfes)
[![Áreas](https://img.shields.io/badge/áreas-5-2e7d32.svg)](#las-cinco-áreas)

</div>

---

Genera preguntas de selección múltiple con única respuesta para las cinco
pruebas del examen Saber 11.°, con la **metadata pedagógica oficial** que el
ICFES usa para construirlas —competencia, componente, afirmación, evidencia y
estándar asociado— y una **justificación propia por cada opción**, incluidas
las incorrectas.

Las preguntas pueden ser de solo texto o de **imagen + texto**: la skill
genera el PNG del estímulo (gráficas, diagramas, planos cartesianos, avisos)
sin depender de que alguien aporte la imagen.

La salida es un **`paquete.zip`** en el formato abierto
[`preguntas-icfes`](https://github.com/Riskbreaker2077/preguntas-icfes),
validado antes de escribirse contra la implementación de referencia del propio
estándar.

## Qué la hace distinta de pedirle preguntas a un chat

- **Taxonomía literal, no inventada.** `competencia`, `componente`,
  `afirmacion` y `evidencia` se copian palabra por palabra de las guías de
  orientación y los marcos de referencia del ICFES. Un consumidor puede
  agrupar por cadena exacta.
- **Las reglas de redacción del ICFES son parte del proceso**, no una
  sugerencia: sin nombres propios, sin «todas las anteriores», sin opciones
  que delaten la clave por longitud o registro, con la clave repartida entre
  las cuatro posiciones. Salen del *Manual para la construcción de ítems*
  (C1.1.M01).
- **Procedencia honesta.** Todo lo que genera queda marcado como
  `ia_generada` y `verificado: false`. Marcar una pregunta como verificada es
  potestad de quien la revisó.
- **Se valida, no se promete.** El ZIP no se escribe si el paquete incumple
  cualquiera de las 13 invariantes del estándar.

## Instalación

```bash
git clone https://github.com/Riskbreaker2077/skill-preguntas-saber-11.git \
  ~/.claude/skills/preguntas-saber-11
```

Necesita **Python 3** con [Pillow](https://pypi.org/project/pillow/) (para las
imágenes) y **Node.js** (para el validador de referencia).

```bash
python3 -c "import PIL; print(PIL.__version__)" && node --version
```

Los PDF originales del ICFES no vienen en el repo por peso; la skill no los
necesita, porque lee `Base_MD/`. Si los quieres, `Base_MD/MANIFEST.md` y
`Base/MANIFEST.txt` conservan título, código y URL de cada uno.

## Uso

En Claude Code, basta con pedirlo:

> «Necesito 10 preguntas tipo ICFES de Ciencias Naturales sobre indagación,
> tres de ellas con gráfica.»

> «Arma un simulacro de Lectura Crítica de 15 preguntas con la distribución
> real de tipos de texto.»

La skill pregunta lo que falte (área, cantidad, enfoque, imágenes), escribe el
paquete, genera las imágenes, valida y entrega la ruta del ZIP con un resumen
de cómo quedó repartido.

### A mano, sin la skill

```bash
# generar las imágenes de una carpeta de trabajo
python3 scripts/imagen.py --lote salida/mi-paquete/_specs salida/mi-paquete/imagenes

# validar sin escribir el ZIP
python3 scripts/empaquetar.py salida/mi-paquete --solo-validar

# validar y empaquetar
python3 scripts/empaquetar.py salida/mi-paquete -o entrega/simulacro.zip
```

Pruébalo con el ejemplo incluido:

```bash
python3 scripts/empaquetar.py ejemplos/ciencias-pendulo --solo-validar
```

## Las cinco áreas

| Área | Preguntas en la prueba real | Referencia |
|---|---|---|
| Matemáticas | 40 | [`referencias/matematicas.md`](referencias/matematicas.md) |
| Lectura Crítica | 41 | [`referencias/lectura-critica.md`](referencias/lectura-critica.md) |
| Sociales y Ciudadanas | 50 | [`referencias/sociales-ciudadanas.md`](referencias/sociales-ciudadanas.md) |
| Ciencias Naturales | 58 | [`referencias/ciencias-naturales.md`](referencias/ciencias-naturales.md) |
| Inglés | 55 (45 calificadas) | [`referencias/ingles.md`](referencias/ingles.md) |

Cada referencia trae la tabla completa de competencias, afirmaciones y
evidencias; los valores válidos de `componente`; los porcentajes oficiales de
distribución; ejemplos de `estandar_asociado`; y cuándo el área pide imagen.

Inglés tiene estructura propia: siete partes, clasificación por nivel MCER, y
tres de esas partes se representan con **grupos** del formato
(emparejamiento con banco de opciones, y pasajes con espacios en blanco).

## Tipos de imagen que genera

`scripts/imagen.py` dibuja sobre Pillow, a 2× y reducido con LANCZOS. Sin
matplotlib, sin cabezas de navegador, sin red.

| Tipo | Para qué |
|---|---|
| `barras` | Comparar categorías, una o varias series |
| `lineas` | Evolución en el tiempo |
| `dispersion` | Relación entre dos variables numéricas |
| `torta` | Reparto de un total |
| `cartesiano` | Funciones y puntos en el plano, con ejes y flechas |
| `esquema` | Cajas y flechas: redes tróficas, procesos, ciclos, mapas conceptuales |
| `aviso` | Letreros y señales (parte 2 de Inglés, textos discontinuos) |

Especificación de cada uno en [`referencias/imagenes.md`](referencias/imagenes.md).
Cuando el estímulo es tabular, la skill usa el bloque nativo `tabla` del
formato en vez de una imagen: se lee con lector de pantalla y no se pixela.

## Mapa del repo

| Ruta | Qué es |
|---|---|
| `SKILL.md` | La skill: flujo, reglas innegociables, mapa de referencias |
| `referencias/` | Taxonomías por área, reglas de construcción de ítems, contrato del formato, guía de imágenes |
| `scripts/imagen.py` | Genera PNG desde una especificación JSON |
| `scripts/empaquetar.py` | Valida y arma el ZIP |
| `scripts/vendor/validar.js` | Validador de referencia del estándar (copia verbatim, MIT) |
| `plantillas/paquete.json` | Esqueleto de un paquete |
| `ejemplos/ciencias-pendulo/` | Paquete completo y válido: un grupo con imagen, una pregunta con tabla |
| `Base_MD/` | Los 20 documentos oficiales del ICFES en Markdown (~1,1 MB) |
| `Base/` | Los PDF originales (no versionados) |

## La base documental

20 documentos oficiales, 656 páginas, convertidos a Markdown con
`pymupdf4llm`:

| Categoría | Documentos |
|---|---|
| Marco metodológico | Manual para la construcción de ítems (C1.1.M01, 2009) · Guía introductoria de Diseño Centrado en Evidencias |
| Guías de orientación | Saber 11.° 2025-1, 2026-1 y 2026-2 |
| Marcos de referencia | Lectura Crítica · Matemáticas · Sociales y Ciudadanas · Ciencias Naturales · Inglés |
| Caja de herramientas | 5 documentos de preguntas explicadas · 5 cuadernillos de práctica de aplicaciones anteriores |

Los cuadernillos están para **calibrar** el estilo y la dificultad. El manual
del ICFES exige ítems originales, y la skill los escribe originales.

## Licencia

[MIT](LICENSE). `scripts/vendor/validar.js` es copia verbatim del validador de
[`preguntas-icfes`](https://github.com/Riskbreaker2077/preguntas-icfes),
también MIT ([`scripts/vendor/LICENSE-preguntas-icfes`](scripts/vendor/LICENSE-preguntas-icfes)).

Los documentos de `Base_MD/` son obras del **Icfes**, incluidas aquí como base
de consulta; sus términos de uso son los del Instituto.
