#!/usr/bin/env python3
"""Próximo id libre de un área, para continuar la numeración de un banco.

    python3 scripts/siguiente_id.py salida/mi-entrega/banco/ciencias-sociales
    python3 scripts/siguiente_id.py ~/banco-preguntas-icfes/banco/ingles --grupo
    python3 scripts/siguiente_id.py <carpeta> --cuantos 20

Sin --cuantos imprime un solo id. Con --cuantos, esa cantidad de ids
consecutivos, uno por línea, listos para asignar a un lote nuevo.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import banco as B  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Próximo id libre de un área del banco.")
    ap.add_argument("area", type=Path, help="carpeta del área, p. ej. banco/ingles")
    ap.add_argument("--grupo", action="store_true", help="id de grupo (<prefijo>-g-NNN)")
    ap.add_argument("--cuantos", type=int, default=1, help="cuántos ids consecutivos")
    args = ap.parse_args()

    if not args.area.is_dir():
        print(f"error: no existe la carpeta {args.area}", file=sys.stderr)
        return 1
    area = B.Area(args.area.resolve())
    primero = B.siguiente_id(area, grupo=args.grupo)
    prefijo, ancho = primero.rsplit("-", 1)[0], len(primero.rsplit("-", 1)[1])
    n = int(re.search(r"(\d+)$", primero).group(1))
    for i in range(max(1, args.cuantos)):
        print(f"{prefijo}-{n + i:0{ancho}d}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except B.ErrorBanco as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
