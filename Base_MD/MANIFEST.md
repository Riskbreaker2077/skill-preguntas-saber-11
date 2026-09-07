# Base_MD — Documentación oficial ICFES en Markdown

Conversión de los PDFs de `Base/` a Markdown usando **pymupdf4llm 1.28.2** (la extensión oficial de PyMuPDF optimizada para ingestión por LLMs).

## Estructura

Cada archivo `.md` tiene frontmatter YAML:

```yaml
---
title: "Título del documento"
categoria: metodologia | guia-orientacion | marco-referencia | preguntas-explicadas | cuadernillo-practica
fuente_pdf: "nombre-del-pdf-original.pdf"
fecha_conversion: "YYYY-MM-DD"
herramienta: "pymupdf4llm 1.28.2"
---
```

## Distribución (20 archivos, ~1.1 MB total)

| Categoría | # | Documentos |
|---|---|---|
| **metodologia** | 2 | Manual construcción ítems 2009 (28 pp) • Guía DCE (17 pp) |
| **guia-orientacion** | 3 | Saber 11 2025-1, 2026-1, 2026-2 (61-73 pp c/u) |
| **marco-referencia** | 5 | Lectura Crítica, Matemáticas, Sociales y Ciudadanas, Ciencias Naturales, Inglés (18-58 pp c/u) |
| **preguntas-explicadas** | 5 | Caja de herramientas — explicación pregunta por pregunta (3 pp c/u) |
| **cuadernillo-practica** | 5 | Cuadernillos reales de Saber 11 anterior (24-41 pp c/u) |

## Por qué `pymupdf4llm`

- **Detecta estructura**: identifica headings (`#`, `##`, `###`), listas, tablas y los reconstruye como Markdown nativo (no como texto plano).
- **Maneja imágenes**: las imágenes de portada/figuras quedan como comentarios HTML `<!-- image -->`, no como basura.
- **Rápido**: 1-3 segundos por PDF en CPU, sin GPU, sin modelos pesados.
- **Misma familia que `pymupdf`**: no introduce una toolchain nueva — el resto de Hermes ya usa PyMuPDF para inspección de PDFs.
- **Persistente**: instalado en `/home/camilo/.hermes/hermes-agent/venv/` (visible para todos los `execute_code` y scripts futuros).

## Cómo re-procesar

```bash
/home/camilo/.hermes/hermes-agent/venv/bin/python \
  /mnt/c/Users/camil/Desktop/Desarrollo/skill-preguntas-saber-11/Base_MD/_convertir_base.py
```

El script (`_convertir_base.py`) re-convierte todos los PDFs de `Base/` a MDs en `Base_MD/`, sobrescribiendo.

## Notas técnicas

- Los PDFs son **digitales** (texto embebido), no escaneados, así que no se necesitó OCR.
- `pymupdf4llm` no usa el modelo `pymupdf_layout` por defecto — eso es opcional y pesado; los resultados ya son estructuralmente ricos.
- El PDF del manual CIE-MN004 oficial del ICFES (escaneado, sin texto extraíble) **no** se pudo convertir — se sustituyó por su versión histórica `Manual_construccion_items_ICFES_2009.pdf` que sí tiene texto embebido.
- Total: **647 páginas PDF → ~1.1 MB Markdown estructurado**, ratio de compresión ~17×.