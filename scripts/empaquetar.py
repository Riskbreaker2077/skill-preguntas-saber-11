#!/usr/bin/env python3
"""Valida una carpeta de trabajo y la empaqueta como paquete.zip.

    python3 scripts/empaquetar.py salida/mi-paquete
    python3 scripts/empaquetar.py salida/mi-paquete -o entrega/lectura-01.zip
    python3 scripts/empaquetar.py salida/mi-paquete --solo-validar

La carpeta de trabajo tiene la forma que exige el estándar:

    mi-paquete/
    ├── paquete.json      (obligatorio)
    ├── imagenes/         (solo si hay bloques de tipo imagen)
    └── fuentes/          (solo si alguna pregunta declara "fuentes")

La validación la hace `scripts/vendor/validar.js`, la implementación de
referencia del estándar `preguntas-icfes` — no una reimplementación. Requiere
Node.js. Los errores bloquean el empaquetado; los avisos no.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
VALIDADOR = RAIZ / "vendor" / "validar.js"

EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".webp"}
EXT_FUENTE = {".pdf"}

DRIVER = """
import { validarPaquete } from %(url)s;
import { readFileSync } from "node:fs";
const paquete = JSON.parse(readFileSync(process.env.RUTA_PAQUETE, "utf-8"));
const opciones = JSON.parse(process.env.OPCIONES_VALIDACION);
process.stdout.write(JSON.stringify(validarPaquete(paquete, opciones)));
"""


def _archivos(carpeta: Path) -> list[str]:
    if not carpeta.is_dir():
        return []
    return sorted(p.name for p in carpeta.iterdir() if p.is_file())


def validar(dir_trabajo: Path, paquete: dict) -> list[dict]:
    """Corre el validador de referencia. Devuelve la lista de errores."""
    if shutil.which("node") is None:
        raise SystemExit(
            "error: no se encontró Node.js, necesario para correr el validador de\n"
            "referencia del estándar (scripts/vendor/validar.js). Instálalo, o usa\n"
            "--sin-validar bajo tu propia responsabilidad."
        )
    entorno = dict(
        os.environ,
        RUTA_PAQUETE=str(dir_trabajo / "paquete.json"),
        OPCIONES_VALIDACION=json.dumps({
            "imagenesDisponibles": _archivos(dir_trabajo / "imagenes"),
            "fuentesDisponibles": _archivos(dir_trabajo / "fuentes"),
        }),
    )
    proc = subprocess.run(
        ["node", "--input-type=module", "-e",
         DRIVER % {"url": json.dumps(VALIDADOR.as_uri())}],
        capture_output=True, text=True, env=entorno,
    )
    if proc.returncode != 0:
        raise SystemExit(f"error: el validador falló:\n{proc.stderr.strip()}")
    return json.loads(proc.stdout)["errores"]


def _bloques(paquete: dict):
    """Todos los bloques de contenido del paquete, vengan de donde vengan."""
    for grupo in paquete.get("grupos", []):
        yield from grupo.get("contexto", [])
        for entrada in grupo.get("banco", []):
            yield from entrada.get("contenido", [])
    for p in paquete.get("preguntas", []):
        yield from p.get("contexto", [])
        yield from p.get("enunciado", [])
        for o in p.get("opciones", []):
            yield from o.get("contenido", [])


def revisar(dir_trabajo: Path, paquete: dict) -> tuple[list[str], list[str]]:
    """Comprobaciones propias de Saber 11.° que el estándar no cubre.

    Devuelve (errores, avisos). Los errores son de empaquetado; el resto son
    señales de calidad que conviene mirar antes de entregar.
    """
    errores, avisos = [], []
    preguntas = paquete.get("preguntas", [])

    for carpeta, exts in (("imagenes", EXT_IMAGEN), ("fuentes", EXT_FUENTE)):
        for nombre in _archivos(dir_trabajo / carpeta):
            if Path(nombre).suffix.lower() not in exts:
                errores.append(
                    f"{carpeta}/{nombre}: extensión no admitida por el estándar "
                    f"({', '.join(sorted(exts))})."
                )

    # Lo que empieza por "_" es material de trabajo declarado como tal (p. ej.
    # _specs/, las especificaciones de las imágenes): queda fuera sin avisar.
    for extra in sorted(p.name for p in dir_trabajo.iterdir()
                        if p.name not in {"paquete.json", "imagenes", "fuentes"}
                        and not p.name.startswith(("_", "."))):
        avisos.append(f"'{extra}' no entra al ZIP: solo van paquete.json, "
                      f"imagenes/ y fuentes/.")

    usadas = {b["archivo"] for b in _bloques(paquete) if b.get("tipo") == "imagen"}
    for huerfana in sorted(set(_archivos(dir_trabajo / "imagenes")) - usadas):
        avisos.append(f"imagenes/{huerfana} no la referencia ninguna pregunta.")

    sin_alt = [b["archivo"] for b in _bloques(paquete)
               if b.get("tipo") == "imagen" and not b.get("descripcion_accesible")]
    for archivo in sorted(set(sin_alt)):
        avisos.append(f"imagenes/{archivo} no tiene 'descripcion_accesible'.")

    claves = Counter()
    for p in preguntas:
        for o in p.get("opciones", []):
            if o.get("es_correcta"):
                claves[o.get("id")] += 1
    if claves and len(preguntas) >= 8:
        techo = max(claves.values())
        if techo > sum(claves.values()) * 0.45:
            reparto = ", ".join(f"{k}: {v}" for k, v in sorted(claves.items()))
            avisos.append(
                f"la clave está desbalanceada ({reparto}). El manual del ICFES pide "
                f"repartirla proporcionalmente entre las posiciones."
            )

    for p in preguntas:
        n = len(p.get("opciones", []))
        if p.get("tipo_item", "estandar") == "estandar" and n and n != 4:
            avisos.append(f"{p.get('id')}: tiene {n} opciones; Saber 11.° usa 4 "
                          f"(salvo las partes 2 a 5 de Inglés, que usan 3).")

    for p in preguntas:
        proc = p.get("procedencia") or {}
        if not proc:
            avisos.append(f"{p.get('id')}: sin 'procedencia'. Una pregunta generada "
                          f"debe declararse como 'ia_generada'.")

    return errores, avisos


def empaquetar(dir_trabajo: Path, salida: Path) -> Path:
    salida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(dir_trabajo / "paquete.json", "paquete.json")
        for carpeta in ("imagenes", "fuentes"):
            for nombre in _archivos(dir_trabajo / carpeta):
                z.write(dir_trabajo / carpeta / nombre, f"{carpeta}/{nombre}")
    return salida


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Valida y empaqueta un paquete de preguntas ICFES.")
    ap.add_argument("carpeta", type=Path, help="carpeta de trabajo con paquete.json")
    ap.add_argument("-o", "--salida", type=Path,
                    help="ruta del .zip (por defecto, <carpeta>.zip)")
    ap.add_argument("--solo-validar", action="store_true",
                    help="valida y reporta, sin escribir el ZIP")
    ap.add_argument("--sin-validar", action="store_true",
                    help="empaqueta sin correr el validador (no recomendado)")
    args = ap.parse_args()

    dir_trabajo = args.carpeta.resolve()
    ruta_json = dir_trabajo / "paquete.json"
    if not ruta_json.is_file():
        print(f"error: no existe {ruta_json}", file=sys.stderr)
        return 1
    try:
        paquete = json.loads(ruta_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: paquete.json no es JSON válido — línea {e.lineno}, "
              f"columna {e.colno}: {e.msg}", file=sys.stderr)
        return 1

    errores_est = [] if args.sin_validar else validar(dir_trabajo, paquete)
    errores_zip, avisos = revisar(dir_trabajo, paquete)

    for e in errores_est:
        donde = f"[{e['pregunta_id']}] " if e.get("pregunta_id") else ""
        print(f"✗ {donde}{e['campo']}: {e['mensaje']}", file=sys.stderr)
    for e in errores_zip:
        print(f"✗ {e}", file=sys.stderr)
    for a in avisos:
        print(f"⚠ {a}", file=sys.stderr)

    if errores_est or errores_zip:
        print(f"\n{len(errores_est) + len(errores_zip)} error(es): el paquete NO se "
              f"empaquetó.", file=sys.stderr)
        return 1

    n_preg = len(paquete.get("preguntas", []))
    n_grupos = len(paquete.get("grupos", []))
    n_img = len(_archivos(dir_trabajo / "imagenes"))
    resumen = (f"{n_preg} pregunta(s), {n_grupos} grupo(s), {n_img} imagen(es)"
               f" — estándar v{paquete.get('version_estandar')}")

    if args.solo_validar:
        print(f"✓ paquete válido: {resumen}")
        return 0

    salida = args.salida or dir_trabajo.with_suffix(".zip")
    empaquetar(dir_trabajo, salida)
    print(f"✓ paquete válido: {resumen}")
    print(f"✓ {salida}  ({salida.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
