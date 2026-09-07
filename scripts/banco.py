#!/usr/bin/env python3
"""Lectura de un banco de preguntas en disco: una pregunta por archivo.

Forma del banco, igual que en `banco-preguntas-icfes`:

    banco/
      <area-slug>/
        <id>.json            una pregunta (schema/v1/pregunta.schema.json)
        grupos/
          <prefijo>-g-NNN.json   un grupo
        imagenes/
          <id>-1.png         prefijadas con el id de su pregunta o grupo
        fuentes/
          <slug>.pdf         PDF de origen, referenciado por "fuentes"

El estándar `preguntas-icfes` valida paquetes, no archivos sueltos, así que
para validar un banco se envuelven sus archivos en un paquete sintético. Es
la misma técnica de `scripts/validar-banco.mjs` en el repo del banco.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# slug de área -> prefijo de id, igual que el areas.json del banco.
AREAS = {
    "ciencias-sociales": "cs",
    "matematicas": "mt",
    "lenguaje": "lg",
    "ciencias-naturales": "cn",
    "ingles": "in",
}

# Nombre legible de cada área, para el campo "area" del paquete y los informes.
NOMBRES = {
    "ciencias-sociales": "Sociales y Ciudadanas",
    "matematicas": "Matemáticas",
    "lenguaje": "Lectura Crítica",
    "ciencias-naturales": "Ciencias Naturales",
    "ingles": "Inglés",
}

VERSION_ESTANDAR = "1.4.0"
EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".webp"}
EXT_FUENTE = {".pdf"}


class ErrorBanco(Exception):
    """El banco en disco no tiene la forma esperada."""


class Area:
    """Las preguntas, grupos e imágenes de una carpeta de área."""

    def __init__(self, carpeta: Path):
        self.carpeta = carpeta
        self.slug = carpeta.name
        self.preguntas = [self._leer(p) for p in sorted(carpeta.glob("*.json"))]
        self.grupos = [self._leer(p) for p in sorted((carpeta / "grupos").glob("*.json"))]

    @staticmethod
    def _leer(ruta: Path) -> dict:
        try:
            dato = json.loads(ruta.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ErrorBanco(f"{ruta}: JSON inválido — línea {e.lineno}, "
                             f"columna {e.colno}: {e.msg}") from None
        if not isinstance(dato, dict):
            raise ErrorBanco(f"{ruta}: se esperaba un objeto JSON.")
        dato["_ruta"] = str(ruta)
        return dato

    def archivos(self, sub: str) -> list[str]:
        carpeta = self.carpeta / sub
        if not carpeta.is_dir():
            return []
        return sorted(p.name for p in carpeta.iterdir() if p.is_file())

    def envolver(self, nombre: str) -> dict:
        """Paquete sintético para pasarle el área al validador de referencia."""
        limpio = lambda d: {k: v for k, v in d.items() if k != "_ruta"}
        return {
            "estandar": "preguntas-icfes",
            "version_estandar": VERSION_ESTANDAR,
            "nombre": nombre,
            "area": NOMBRES.get(self.slug, self.slug),
            "grupos": [limpio(g) for g in self.grupos],
            "preguntas": [limpio(p) for p in self.preguntas],
        }

    def __repr__(self):
        return (f"<Area {self.slug}: {len(self.preguntas)} preguntas, "
                f"{len(self.grupos)} grupos>")


def cargar(raiz: Path) -> list[Area]:
    """Todas las áreas bajo `raiz` (la carpeta que contiene las de área)."""
    if not raiz.is_dir():
        raise ErrorBanco(f"no existe la carpeta {raiz}")
    areas = [Area(d) for d in sorted(raiz.iterdir())
             if d.is_dir() and not d.name.startswith(("_", "."))]
    if not areas:
        raise ErrorBanco(f"{raiz} no contiene ninguna carpeta de área "
                         f"({', '.join(sorted(AREAS))}).")
    vacias = [a.slug for a in areas if not a.preguntas]
    if vacias:
        raise ErrorBanco(f"sin preguntas en: {', '.join(vacias)}")
    return areas


def _mayor(a: str, b: str) -> str:
    parte = lambda v: tuple(int(x) for x in v.split("."))
    return a if parte(a) >= parte(b) else b


def version_minima(pregunta: dict) -> str:
    """Versión mínima del estándar que exigen los campos que usa la pregunta.

    Réplica de `calcularVersionMinima` en scripts/vendor/validar.js: si las
    dos divergen, el validador rechaza la pregunta.
    """
    minima = "1.0.0"
    if any(pregunta.get(c) is not None
           for c in ("grado", "prueba", "procedencia", "verificado", "fuentes")):
        minima = _mayor(minima, "1.1.0")
    for o in pregunta.get("opciones") or []:
        if o.get("procedencia_justificacion") is not None or \
           o.get("justificacion_verificada") is not None:
            minima = _mayor(minima, "1.1.0")
    if any(pregunta.get(c) is not None
           for c in ("grupo_id", "tipo_item", "nivel_mcer", "valor")):
        minima = _mayor(minima, "1.2.0")
    opciones = pregunta.get("opciones")
    if isinstance(opciones, list) and len(opciones) >= 2 and len(opciones) != 4:
        minima = _mayor(minima, "1.2.0")
    return minima


def siguiente_id(area: Area, *, grupo: bool = False) -> str:
    """Próximo id libre del área, continuando su numeración."""
    prefijo = AREAS.get(area.slug)
    if prefijo is None:
        raise ErrorBanco(f"área desconocida '{area.slug}'; las conocidas son "
                         f"{', '.join(sorted(AREAS))}.")
    patron = re.compile(rf"^{prefijo}-g-(\d+)$" if grupo else rf"^{prefijo}-(\d+)$")
    fuente = area.grupos if grupo else area.preguntas
    usados = [int(m.group(1)) for d in fuente
              if (m := patron.match(str(d.get("id", ""))))]
    n = max(usados, default=0) + 1
    return f"{prefijo}-g-{n:03d}" if grupo else f"{prefijo}-{n:03d}"
