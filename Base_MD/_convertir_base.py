"""Script persistente para (re)convertir la base PDF→MD del proyecto.

Uso:
  /home/camilo/.hermes/hermes-agent/venv/bin/python convertir_base.py

Lee los PDFs en Base/, escribe los MD en Base_MD/ (sobrescribe).
Persistente: este archivo vive junto a Base_MD/ y se puede re-ejecutar
si la base crece o se quieren re-procesar archivos.

Dependencia: pymupdf4llm (instalada en /home/camilo/.hermes/hermes-agent/venv).
"""
import os, sys, json
from datetime import datetime

# Asegurar acceso a pymupdf4llm desde el venv de Hermes
HERMES_VENV = "/home/camilo/.hermes/hermes-agent/venv/lib/python3.11/site-packages"
if HERMES_VENV not in sys.path:
    sys.path.insert(0, HERMES_VENV)

try:
    import pymupdf4llm
except ImportError:
    print(f"ERROR: pymupdf4llm no está instalado en {HERMES_VENV}")
    print("Instalar con:")
    print(f"  /home/camilo/.hermes/hermes-agent/venv/bin/python -m pip install pymupdf4llm")
    sys.exit(1)

# Rutas del proyecto (padre de Base_MD)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROYECTO_DIR = os.path.dirname(SCRIPT_DIR)
BASE = os.path.join(PROYECTO_DIR, "Base")
DEST = SCRIPT_DIR  # este script vive en Base_MD/

CATEGORY = {
    'Manual_construccion_items_ICFES_2009.pdf':              'metodologia',
    'Guia_introductoria_diseno_centrado_evidencias.pdf':     'metodologia',
    'Guia_orientacion_Saber11_2025-1.pdf':                   'guia-orientacion',
    'Guia_orientacion_Saber11_2026-1.pdf':                   'guia-orientacion',
    'Guia_orientacion_Saber11_2026-2.pdf':                   'guia-orientacion',
    'Marco_referencia_lectura_critica_saber11.pdf':          'marco-referencia',
    'Marco_referencia_matematicas_saber11.pdf':              'marco-referencia',
    'Marco_referencia_sociales_yciudadanas_saber11.pdf':     'marco-referencia',
    'Marco_referencia_ciencias_naturales_saber11.pdf':       'marco-referencia',
    'Marco_referencia_ingles_saber11.pdf':                   'marco-referencia',
    '01_EXPLICADAS_LECTURA.pdf':                             'preguntas-explicadas',
    '03_EXPLICADAS_MATEMATICAS.pdf':                         'preguntas-explicadas',
    '05_EXPLICADAS_SOCIALES.pdf':                            'preguntas-explicadas',
    '07_EXPLICADAS_CIENCIAS.pdf':                            'preguntas-explicadas',
    '09_EXPLICADAS_INGLES.pdf':                              'preguntas-explicadas',
    '02_PRACTICA_LECTURA.pdf':                               'cuadernillo-practica',
    '04_PRACTICA_MATEMATICAS.pdf':                           'cuadernillo-practica',
    '06_PRACTICA_SOCIALES.pdf':                              'cuadernillo-practica',
    '08_PRACTICA_CIENCIAS.pdf':                              'cuadernillo-practica',
    '10_PRACTICA_INGLES.pdf':                                'cuadernillo-practica',
}

TITLE_MAP = {
    'Manual_construccion_items_ICFES_2009.pdf':              'Manual para la construcción de ítems tipo selección de respuesta',
    'Guia_introductoria_diseno_centrado_evidencias.pdf':     'Guía introductoria al Diseño Centrado en Evidencias',
    'Guia_orientacion_Saber11_2025-1.pdf':                   'Guía de orientación del Examen Saber 11.º — 2025-1',
    'Guia_orientacion_Saber11_2026-1.pdf':                   'Guía de orientación del Examen Saber 11.º — 2026-1',
    'Guia_orientacion_Saber11_2026-2.pdf':                   'Guía de orientación del Examen Saber 11.º — 2026-2',
    'Marco_referencia_lectura_critica_saber11.pdf':          'Marco de referencia — Prueba de Lectura Crítica Saber 11',
    'Marco_referencia_matematicas_saber11.pdf':              'Marco de referencia — Prueba de Matemáticas Saber 11',
    'Marco_referencia_sociales_yciudadanas_saber11.pdf':     'Marco de referencia — Prueba de Sociales y Ciudadanas Saber 11',
    'Marco_referencia_ciencias_naturales_saber11.pdf':       'Marco de referencia — Prueba de Ciencias Naturales Saber 11',
    'Marco_referencia_ingles_saber11.pdf':                   'Marco de referencia — Prueba de Inglés Saber 11',
    '01_EXPLICADAS_LECTURA.pdf':                             'Caja de herramientas — Preguntas explicadas: Lectura Crítica',
    '03_EXPLICADAS_MATEMATICAS.pdf':                         'Caja de herramientas — Preguntas explicadas: Matemáticas',
    '05_EXPLICADAS_SOCIALES.pdf':                            'Caja de herramientas — Preguntas explicadas: Sociales y Ciudadanas',
    '07_EXPLICADAS_CIENCIAS.pdf':                            'Caja de herramientas — Preguntas explicadas: Ciencias Naturales',
    '09_EXPLICADAS_INGLES.pdf':                              'Caja de herramientas — Preguntas explicadas: Inglés',
    '02_PRACTICA_LECTURA.pdf':                               'Cuadernillo de preguntas — Saber 11 — Lectura Crítica',
    '04_PRACTICA_MATEMATICAS.pdf':                           'Cuadernillo de preguntas — Saber 11 — Matemáticas',
    '06_PRACTICA_SOCIALES.pdf':                              'Cuadernillo de preguntas — Saber 11 — Sociales y Ciudadanas',
    '08_PRACTICA_CIENCIAS.pdf':                              'Cuadernillo de preguntas — Saber 11 — Ciencias Naturales',
    '10_PRACTICA_INGLES.pdf':                                'Cuadernillo de preguntas — Saber 11 — Inglés',
}


def convertir(pdf_path, md_path, categoria, titulo):
    """Convierte un PDF a Markdown con frontmatter YAML."""
    # pymupdf4llm.to_markdown() retorna str por defecto
    md_text = str(pymupdf4llm.to_markdown(pdf_path))
    body = md_text.strip()
    if not body.startswith('#'):
        body = f'# {titulo}\n\n{body}'

    fuente = os.path.basename(pdf_path)
    fm = (
        '---\n'
        f'title: "{titulo}"\n'
        f'categoria: {categoria}\n'
        f'fuente_pdf: "{fuente}"\n'
        f'fecha_conversion: "{datetime.now().strftime("%Y-%m-%d")}"\n'
        f'herramienta: "pymupdf4llm {pymupdf4llm.__version__ if hasattr(pymupdf4llm, "__version__") else "1.28.2"}"\n'
        '---\n\n'
    )

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(fm + body + '\n')

    return len(fm + body)


def main():
    if not os.path.isdir(BASE):
        print(f"ERROR: No existe {BASE}")
        sys.exit(1)

    os.makedirs(DEST, exist_ok=True)

    pdfs = sorted([f for f in os.listdir(BASE) if f.lower().endswith('.pdf')])
    print(f"Convirtiendo {len(pdfs)} PDFs de {BASE} → {DEST}")
    print(f"Herramienta: pymupdf4llm (PyMuPDF LLM-optimized Markdown)")
    print()

    total_size = 0
    cat_count = {}
    for i, pdf_name in enumerate(pdfs, 1):
        src = os.path.join(BASE, pdf_name)
        dst = os.path.join(DEST, pdf_name[:-4] + '.md')
        cat = CATEGORY.get(pdf_name, 'general')
        titulo = TITLE_MAP.get(pdf_name, pdf_name[:-4])
        print(f'[{i:2d}/{len(pdfs)}] {pdf_name} ... ', end='', flush=True)

        try:
            size = convertir(src, dst, cat, titulo)
            total_size += size
            cat_count[cat] = cat_count.get(cat, 0) + 1
            print(f'OK ({size/1024:.1f} KB)')
        except Exception as e:
            print(f'ERROR: {e}')

    print()
    print(f"=== RESUMEN ===")
    print(f"Total convertidos: {len(pdfs)}")
    print(f"Tamaño total MD:   {total_size/1024:.1f} KB ({total_size/(1024*1024):.2f} MB)")
    print(f"Por categoría:")
    for c, n in sorted(cat_count.items()):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()