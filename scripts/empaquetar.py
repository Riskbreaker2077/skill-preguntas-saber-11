#!/usr/bin/env python3
"""Valida un banco de preguntas y lo empaqueta como ZIP, un JSON por pregunta.

    python3 scripts/empaquetar.py salida/mi-entrega
    python3 scripts/empaquetar.py salida/mi-entrega -o entrega/sociales.zip
    python3 scripts/empaquetar.py salida/mi-entrega --solo-validar

La carpeta de trabajo contiene un árbol `banco/` con la forma que describe
`referencias/formato-paquete.md`:

    salida/mi-entrega/
    └── banco/
        └── ciencias-sociales/
            ├── cs-155.json      una pregunta por archivo
            ├── grupos/cs-g-002.json
            ├── imagenes/cs-170-1.png
            └── fuentes/cuadernillo-2024.pdf

El ZIP reproduce ese árbol, así que se descomprime encima de un banco
existente sin tocar nada más. La validación envuelve cada área en un paquete
sintético y la pasa por `scripts/vendor/validar.js`, la implementación de
referencia del estándar. Requiere Node.js. Los errores bloquean el
empaquetado; los avisos no.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import banco as B  # noqa: E402

VALIDADOR = Path(__file__).resolve().parent / "vendor" / "validar.js"

DRIVER = """
import { validarPaquete } from %(url)s;
import { readFileSync } from "node:fs";
const paquete = JSON.parse(readFileSync(process.env.RUTA_PAQUETE, "utf-8"));
const opciones = JSON.parse(process.env.OPCIONES_VALIDACION);
process.stdout.write(JSON.stringify(validarPaquete(paquete, opciones)));
"""


def validar(area: B.Area) -> list[dict]:
    """Corre el validador de referencia sobre un área envuelta en un paquete."""
    if shutil.which("node") is None:
        raise SystemExit(
            "error: no se encontró Node.js, necesario para correr el validador de\n"
            "referencia del estándar (scripts/vendor/validar.js). Instálalo, o usa\n"
            "--sin-validar bajo tu propia responsabilidad."
        )
    envoltura = area.envolver(f"Validación de {area.slug}")
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8",
                                     delete=False) as f:
        json.dump(envoltura, f, ensure_ascii=False)
        ruta = f.name
    try:
        proc = subprocess.run(
            ["node", "--input-type=module", "-e",
             DRIVER % {"url": json.dumps(VALIDADOR.as_uri())}],
            capture_output=True, text=True,
            env=dict(os.environ, RUTA_PAQUETE=ruta, OPCIONES_VALIDACION=json.dumps({
                "imagenesDisponibles": area.archivos("imagenes"),
                "fuentesDisponibles": area.archivos("fuentes"),
            })),
        )
    finally:
        os.unlink(ruta)
    if proc.returncode != 0:
        raise SystemExit(f"error: el validador falló:\n{proc.stderr.strip()}")
    return json.loads(proc.stdout)["errores"]


def _bloques(area: B.Area):
    for g in area.grupos:
        yield from g.get("contexto", [])
        for entrada in g.get("banco", []):
            yield from entrada.get("contenido", [])
    for p in area.preguntas:
        yield from p.get("contexto", [])
        yield from p.get("enunciado", [])
        for o in p.get("opciones", []):
            yield from o.get("contenido", [])


def revisar(area: B.Area) -> tuple[list[str], list[str]]:
    """Comprobaciones propias del banco y de Saber 11.° que el estándar no cubre."""
    errores, avisos = [], []
    ids = {str(d.get("id")) for d in area.preguntas + area.grupos}

    # El banco localiza cada pregunta por su nombre de archivo: deben coincidir.
    for d in area.preguntas + area.grupos:
        ruta = Path(d["_ruta"])
        if ruta.stem != str(d.get("id")):
            errores.append(f"{ruta.name}: el archivo debería llamarse "
                           f"{d.get('id')}.json, como su id.")

    for sub, exts in (("imagenes", B.EXT_IMAGEN), ("fuentes", B.EXT_FUENTE)):
        for nombre in area.archivos(sub):
            if Path(nombre).suffix.lower() not in exts:
                errores.append(f"{area.slug}/{sub}/{nombre}: extensión no admitida "
                               f"({', '.join(sorted(exts))}).")

    # Convención del banco: la imagen se llama <id-de-quien-la-usa>-N.ext
    for nombre in area.archivos("imagenes"):
        m = re.match(r"^(.+)-(\d+)$", Path(nombre).stem)
        if not m or m.group(1) not in ids:
            avisos.append(f"imagenes/{nombre}: el nombre no empieza por el id de una "
                          f"pregunta o grupo del área, como pide la convención "
                          f"<id>-N.png.")

    usadas = {b["archivo"] for b in _bloques(area) if b.get("tipo") == "imagen"}
    for huerfana in sorted(set(area.archivos("imagenes")) - usadas):
        avisos.append(f"imagenes/{huerfana} no la referencia ninguna pregunta.")

    for archivo in sorted({b["archivo"] for b in _bloques(area)
                           if b.get("tipo") == "imagen"
                           and not b.get("descripcion_accesible")}):
        avisos.append(f"imagenes/{archivo} no tiene 'descripcion_accesible'.")

    for p in area.preguntas:
        pid = p.get("id")
        declarada = p.get("version_estandar")
        if not declarada:
            avisos.append(f"{pid}: sin 'version_estandar'. Un archivo suelto es lo "
                          f"único que tiene para autodescribirse; debería declarar "
                          f"{B.version_minima(p)}.")
        if not p.get("procedencia"):
            avisos.append(f"{pid}: sin 'procedencia'. Una pregunta generada debe "
                          f"declararse como 'ia_generada'.")
        # Saber 11.° usa 4 opciones, salvo las partes 2 a 5 de Inglés, que usan 3
        # por diseño oficial: en esa área 3 no es un defecto y no se avisa.
        admitidas = {3, 4} if area.slug == "ingles" else {4}
        n = len(p.get("opciones", []))
        if p.get("tipo_item", "estandar") == "estandar" and n and n not in admitidas:
            avisos.append(f"{pid}: tiene {n} opciones; aquí se esperan "
                          f"{' o '.join(str(x) for x in sorted(admitidas))}.")

    claves = Counter(o.get("id") for p in area.preguntas
                     for o in p.get("opciones", []) if o.get("es_correcta"))
    if claves and len(area.preguntas) >= 8 and max(claves.values()) > sum(claves.values()) * 0.45:
        reparto = ", ".join(f"{k}: {v}" for k, v in sorted(claves.items()))
        avisos.append(f"la clave está desbalanceada ({reparto}). El manual del ICFES "
                      f"pide repartirla proporcionalmente entre las posiciones.")

    return errores, avisos


def empaquetar(raiz_banco: Path, salida: Path) -> Path:
    salida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for archivo in sorted(raiz_banco.rglob("*")):
            if archivo.is_file() and not archivo.name.startswith("."):
                z.write(archivo, str(archivo.relative_to(raiz_banco.parent)))
    return salida


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Valida un banco de preguntas y lo empaqueta como ZIP.")
    ap.add_argument("carpeta", type=Path, help="carpeta de trabajo que contiene banco/")
    ap.add_argument("-o", "--salida", type=Path,
                    help="ruta del .zip (por defecto, <carpeta>.zip)")
    ap.add_argument("--solo-validar", action="store_true",
                    help="valida y reporta, sin escribir el ZIP")
    ap.add_argument("--sin-validar", action="store_true",
                    help="empaqueta sin correr el validador (no recomendado)")
    args = ap.parse_args()

    raiz = args.carpeta.resolve() / "banco"
    try:
        areas = B.cargar(raiz)
    except B.ErrorBanco as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    n_err = 0
    for area in areas:
        errores = [] if args.sin_validar else validar(area)
        errores_banco, avisos = revisar(area)
        for e in errores:
            donde = f"[{e['pregunta_id']}] " if e.get("pregunta_id") else ""
            print(f"✗ {area.slug}: {donde}{e['campo']}: {e['mensaje']}", file=sys.stderr)
        for e in errores_banco:
            print(f"✗ {area.slug}: {e}", file=sys.stderr)
        for a in avisos:
            print(f"⚠ {area.slug}: {a}", file=sys.stderr)
        n_err += len(errores) + len(errores_banco)

    if n_err:
        print(f"\n{n_err} error(es): no se empaquetó nada.", file=sys.stderr)
        return 1

    for area in areas:
        print(f"✓ {area.slug}: {len(area.preguntas)} pregunta(s), "
              f"{len(area.grupos)} grupo(s), {len(area.archivos('imagenes'))} imagen(es)")
    if args.solo_validar:
        return 0

    salida = args.salida or args.carpeta.resolve().with_suffix(".zip")
    empaquetar(raiz, salida)
    total = sum(len(a.preguntas) for a in areas)
    print(f"✓ {salida}  ({salida.stat().st_size / 1024:.1f} KB, "
          f"{total} archivos de pregunta)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except B.ErrorBanco as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
