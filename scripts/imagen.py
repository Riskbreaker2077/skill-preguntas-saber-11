#!/usr/bin/env python3
"""Genera la imagen de una pregunta a partir de una especificación JSON.

    python3 scripts/imagen.py spec.json salida.png
    python3 scripts/imagen.py --lote specs/ imagenes/

Tipos soportados: barras, lineas, dispersion, torta, cartesiano, esquema,
aviso. La especificación de cada uno está en referencias/imagenes.md.

Única dependencia: Pillow. Se dibuja a 2x y se reduce con LANCZOS, así que
las líneas y el texto salen suavizados sin depender de matplotlib.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ESCALA = 2  # supermuestreo

FUENTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "C:/Windows/Fonts/arial.ttf",
]
FUENTES_NEGRITA = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

TINTA = (26, 26, 26)
GRIS = (120, 120, 120)
REJILLA = (222, 222, 222)
FONDO = (255, 255, 255)

# Paleta de series: contrastes distintos también al imprimir en escala de grises.
PALETA = [
    (37, 78, 148),    # azul
    (196, 92, 22),    # naranja quemado
    (58, 125, 68),    # verde
    (140, 60, 130),   # morado
    (176, 40, 48),    # rojo
    (90, 90, 90),     # gris
]


class ErrorSpec(Exception):
    """La especificación no describe una imagen que se pueda dibujar."""


def _fuente(tam: int, negrita: bool = False):
    for ruta in (FUENTES_NEGRITA if negrita else FUENTES):
        try:
            return ImageFont.truetype(ruta, tam * ESCALA)
        except OSError:
            continue
    return ImageFont.load_default()


class Lienzo:
    def __init__(self, ancho: int, alto: int):
        self.ancho, self.alto = ancho, alto
        self.img = Image.new("RGB", (ancho * ESCALA, alto * ESCALA), FONDO)
        self.d = ImageDraw.Draw(self.img)

    def _e(self, *vals):
        return tuple(v * ESCALA for v in vals)

    def linea(self, x1, y1, x2, y2, color=TINTA, grosor=1):
        self.d.line(self._e(x1, y1, x2, y2), fill=color, width=max(1, grosor * ESCALA))

    def rect(self, x1, y1, x2, y2, relleno=None, borde=TINTA, grosor=1):
        self.d.rectangle(self._e(x1, y1, x2, y2), fill=relleno, outline=borde,
                         width=max(1, grosor * ESCALA))

    def elipse(self, x1, y1, x2, y2, relleno=None, borde=TINTA, grosor=1):
        self.d.ellipse(self._e(x1, y1, x2, y2), fill=relleno, outline=borde,
                       width=max(1, grosor * ESCALA))

    def punto(self, x, y, r=4, color=TINTA):
        self.elipse(x - r, y - r, x + r, y + r, relleno=color, borde=color)

    def texto(self, x, y, txt, tam=13, color=TINTA, anclaje="la", negrita=False):
        self.d.text(self._e(x, y), txt, font=_fuente(tam, negrita), fill=color,
                    anchor=anclaje)

    def texto_vertical(self, x, y, txt, tam=13, color=TINTA):
        """Texto girado 90° a la izquierda, centrado en (x, y). Para el eje Y."""
        f = _fuente(tam, False)
        caja = self.d.textbbox((0, 0), txt, font=f)
        w, h = caja[2] - caja[0], caja[3] - caja[1]
        tira = Image.new("RGBA", (w + 4 * ESCALA, h + 4 * ESCALA), (0, 0, 0, 0))
        ImageDraw.Draw(tira).text((2 * ESCALA - caja[0], 2 * ESCALA - caja[1]), txt,
                                  font=f, fill=color)
        tira = tira.rotate(90, expand=True)
        self.img.paste(tira, (int(x * ESCALA - tira.width / 2),
                              int(y * ESCALA - tira.height / 2)), tira)

    def medir(self, txt, tam=13, negrita=False) -> tuple[float, float]:
        caja = self.d.textbbox((0, 0), txt, font=_fuente(tam, negrita))
        return (caja[2] - caja[0]) / ESCALA, (caja[3] - caja[1]) / ESCALA

    def flecha(self, x1, y1, x2, y2, color=TINTA, grosor=2, cabeza=9):
        self.linea(x1, y1, x2, y2, color=color, grosor=grosor)
        ang = math.atan2(y2 - y1, x2 - x1)
        for giro in (2.6, -2.6):
            self.linea(x2, y2,
                       x2 + cabeza * math.cos(ang + giro),
                       y2 + cabeza * math.sin(ang + giro),
                       color=color, grosor=grosor)

    def guardar(self, ruta: Path):
        self.img.resize((self.ancho, self.alto), Image.LANCZOS).save(ruta, "PNG",
                                                                    optimize=True)


# --------------------------------------------------------------------------
# Utilidades de ejes


def _paso_bonito(bruto: float) -> float:
    if bruto <= 0:
        return 1.0
    exp = math.floor(math.log10(bruto))
    base = bruto / (10 ** exp)
    for corte, paso in ((1.5, 1), (3, 2), (7, 5)):
        if base < corte:
            return paso * 10 ** exp
    return 10 ** (exp + 1)


def _marcas(vmin: float, vmax: float, objetivo: int = 6):
    if vmax <= vmin:
        vmax = vmin + 1
    paso = _paso_bonito((vmax - vmin) / objetivo)
    ini = math.floor(vmin / paso) * paso
    fin = math.ceil(vmax / paso) * paso
    vals, v = [], ini
    while v <= fin + paso / 1000:
        vals.append(round(v, 10))
        v += paso
    return vals, ini, fin


def _fmt(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _envolver(lienzo: Lienzo, txt: str, ancho_max: float, tam: int) -> list[str]:
    palabras, lineas, actual = txt.split(), [], ""
    for p in palabras:
        cand = f"{actual} {p}".strip()
        if lienzo.medir(cand, tam)[0] <= ancho_max or not actual:
            actual = cand
        else:
            lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


class _Marco:
    """Área de dibujo con ejes, marcas y leyenda; compartida por las gráficas."""

    def __init__(self, lienzo: Lienzo, spec: dict, con_eje_y=True):
        self.l = lienzo
        self.titulo = spec.get("titulo", "")
        self.eje_x = spec.get("eje_x", "")
        self.eje_y = spec.get("eje_y", "")
        self.x0 = 74 if (con_eje_y and self.eje_y) else 56
        self.x1 = lienzo.ancho - 24
        self.y0 = 46 if self.titulo else 22
        self.y1 = lienzo.alto - (58 if self.eje_x else 44)

    def cabecera(self):
        if self.titulo:
            self.l.texto(self.l.ancho / 2, 16, self.titulo, tam=15, anclaje="ma",
                         negrita=True)
        if self.eje_x:
            self.l.texto((self.x0 + self.x1) / 2, self.l.alto - 16, self.eje_x,
                         tam=12, anclaje="ma", color=GRIS)
        if self.eje_y:
            self.l.texto_vertical(16, (self.y0 + self.y1) / 2, self.eje_y, tam=12,
                                  color=GRIS)

    def eje_vertical(self, vmin, vmax, objetivo=6):
        vals, lo, hi = _marcas(vmin, vmax, objetivo)
        self.lo, self.hi = lo, hi
        for v in vals:
            y = self.py(v)
            self.l.linea(self.x0, y, self.x1, y, color=REJILLA)
            self.l.texto(self.x0 - 8, y, _fmt(v), tam=11, anclaje="rm", color=GRIS)
        self.l.linea(self.x0, self.y0, self.x0, self.y1, grosor=1)
        self.l.linea(self.x0, self.y1, self.x1, self.y1, grosor=1)

    def py(self, v):
        if self.hi == self.lo:
            return self.y1
        return self.y1 - (v - self.lo) / (self.hi - self.lo) * (self.y1 - self.y0)

    def leyenda(self, nombres):
        if len(nombres) < 2:
            return
        x, y = self.x0, self.y1 + 26
        for i, nom in enumerate(nombres):
            col = PALETA[i % len(PALETA)]
            self.l.rect(x, y, x + 12, y + 12, relleno=col, borde=col)
            self.l.texto(x + 18, y + 6, nom, tam=11, anclaje="lm")
            x += 18 + self.l.medir(nom, 11)[0] + 22


# --------------------------------------------------------------------------
# Tipos de imagen


def dibujar_barras(spec: dict) -> Lienzo:
    cats = spec.get("categorias") or []
    series = spec.get("series") or []
    if not cats or not series:
        raise ErrorSpec("'barras' necesita 'categorias' y 'series'.")
    for s in series:
        if len(s.get("valores", [])) != len(cats):
            raise ErrorSpec(
                f"la serie '{s.get('nombre','?')}' tiene "
                f"{len(s.get('valores', []))} valores y hay {len(cats)} categorías."
            )

    l = Lienzo(spec.get("ancho", 620), spec.get("alto", 400))
    m = _Marco(l, spec)
    if len(series) > 1:
        m.y1 -= 26
    m.cabecera()
    todos = [v for s in series for v in s["valores"]]
    m.eje_vertical(min(0, min(todos)), max(todos))

    ancho_cat = (m.x1 - m.x0) / len(cats)
    hueco = ancho_cat * 0.22
    ancho_barra = (ancho_cat - 2 * hueco) / len(series)
    base = m.py(max(m.lo, 0))
    for ci, cat in enumerate(cats):
        cx = m.x0 + ci * ancho_cat
        for si, s in enumerate(series):
            col = PALETA[si % len(PALETA)]
            x = cx + hueco + si * ancho_barra
            y = m.py(s["valores"][ci])
            l.rect(x, min(y, base), x + ancho_barra - 2, max(y, base),
                   relleno=col, borde=col)
            if spec.get("mostrar_valores", True):
                l.texto(x + ancho_barra / 2 - 1, min(y, base) - 5,
                        _fmt(s["valores"][ci]), tam=10, anclaje="md", color=TINTA)
        for j, linea in enumerate(_envolver(l, str(cat), ancho_cat - 4, 11)[:2]):
            l.texto(cx + ancho_cat / 2, m.y1 + 6 + j * 13, linea, tam=11, anclaje="ma")
    m.leyenda([s.get("nombre", "") for s in series])
    return l


def dibujar_lineas(spec: dict) -> Lienzo:
    cats = spec.get("categorias") or []
    series = spec.get("series") or []
    if not cats or not series:
        raise ErrorSpec("'lineas' necesita 'categorias' y 'series'.")

    l = Lienzo(spec.get("ancho", 620), spec.get("alto", 400))
    m = _Marco(l, spec)
    if len(series) > 1:
        m.y1 -= 26
    m.cabecera()
    todos = [v for s in series for v in s["valores"]]
    margen = (max(todos) - min(todos)) * 0.1 or 1
    m.eje_vertical(min(todos) - margen, max(todos) + margen)

    paso = (m.x1 - m.x0) / max(1, len(cats) - 1) if len(cats) > 1 else 0
    xs = [m.x0 + i * paso for i in range(len(cats))]
    for si, s in enumerate(series):
        col = PALETA[si % len(PALETA)]
        pts = [(xs[i], m.py(v)) for i, v in enumerate(s["valores"])]
        for a, b in zip(pts, pts[1:]):
            l.linea(*a, *b, color=col, grosor=2)
        for p in pts:
            l.punto(*p, r=4, color=col)
    for i, cat in enumerate(cats):
        l.texto(xs[i], m.y1 + 6, str(cat), tam=11, anclaje="ma")
    m.leyenda([s.get("nombre", "") for s in series])
    return l


def dibujar_dispersion(spec: dict) -> Lienzo:
    series = spec.get("series") or ([{"nombre": "", "puntos": spec["puntos"]}]
                                    if spec.get("puntos") else [])
    if not series:
        raise ErrorSpec("'dispersion' necesita 'puntos' o 'series'.")

    l = Lienzo(spec.get("ancho", 620), spec.get("alto", 420))
    m = _Marco(l, spec)
    if len(series) > 1:
        m.y1 -= 26
    m.cabecera()
    todos = [p for s in series for p in s["puntos"]]
    ys = [p[1] for p in todos]
    mar_y = (max(ys) - min(ys)) * 0.1 or 1
    m.eje_vertical(min(ys) - mar_y, max(ys) + mar_y)

    xs = [p[0] for p in todos]
    mar_x = (max(xs) - min(xs)) * 0.08 or 1
    marcas_x, xlo, xhi = _marcas(min(xs) - mar_x, max(xs) + mar_x, 6)
    px = lambda v: m.x0 + (v - xlo) / (xhi - xlo) * (m.x1 - m.x0)
    for v in marcas_x:
        l.linea(px(v), m.y1, px(v), m.y1 + 4, color=GRIS)
        l.texto(px(v), m.y1 + 7, _fmt(v), tam=11, anclaje="ma", color=GRIS)
    for si, s in enumerate(series):
        col = PALETA[si % len(PALETA)]
        for x, y in s["puntos"]:
            l.punto(px(x), m.py(y), r=4, color=col)
    m.leyenda([s.get("nombre", "") for s in series])
    return l


def dibujar_torta(spec: dict) -> Lienzo:
    segs = spec.get("segmentos") or []
    if not segs:
        raise ErrorSpec("'torta' necesita 'segmentos'.")
    total = sum(s["valor"] for s in segs)
    if total <= 0:
        raise ErrorSpec("la suma de los segmentos debe ser mayor que cero.")

    l = Lienzo(spec.get("ancho", 560), spec.get("alto", 400))
    if spec.get("titulo"):
        l.texto(l.ancho / 2, 16, spec["titulo"], tam=15, anclaje="ma", negrita=True)

    cx, cy, r = 175, l.alto / 2 + 10, 128
    ang = -90.0
    for i, s in enumerate(segs):
        barrido = s["valor"] / total * 360
        col = PALETA[i % len(PALETA)]
        l.d.pieslice(l._e(cx - r, cy - r, cx + r, cy + r), ang, ang + barrido,
                     fill=col, outline=FONDO, width=2 * ESCALA)
        medio = math.radians(ang + barrido / 2)
        pct = s["valor"] / total * 100
        if pct >= 6:
            l.texto(cx + r * 0.62 * math.cos(medio), cy + r * 0.62 * math.sin(medio),
                    f"{pct:.0f} %", tam=12, color=(255, 255, 255), anclaje="mm",
                    negrita=True)
        ang += barrido

    y = cy - len(segs) * 13
    for i, s in enumerate(segs):
        col = PALETA[i % len(PALETA)]
        l.rect(330, y, 342, y + 12, relleno=col, borde=col)
        etq = f"{s['etiqueta']} ({_fmt(s['valor'])})"
        l.texto(350, y + 6, etq, tam=12, anclaje="lm")
        y += 26
    return l


def dibujar_cartesiano(spec: dict) -> Lienzo:
    curvas = spec.get("curvas") or []
    marcados = spec.get("puntos_marcados") or []
    if not curvas and not marcados:
        raise ErrorSpec("'cartesiano' necesita 'curvas' o 'puntos_marcados'.")

    l = Lienzo(spec.get("ancho", 520), spec.get("alto", 460))
    if spec.get("titulo"):
        l.texto(l.ancho / 2, 16, spec["titulo"], tam=15, anclaje="ma", negrita=True)

    todos = [p for c in curvas for p in c["puntos"]] + \
            [[p["x"], p["y"]] for p in marcados]
    xs, ys = [p[0] for p in todos], [p[1] for p in todos]
    rx = spec.get("rango_x") or [min(xs), max(xs)]
    ry = spec.get("rango_y") or [min(ys), max(ys)]
    mx, my = (rx[1] - rx[0]) * 0.08 or 1, (ry[1] - ry[0]) * 0.1 or 1
    marcas_x, xlo, xhi = _marcas(rx[0] - mx, rx[1] + mx, 8)
    marcas_y, ylo, yhi = _marcas(ry[0] - my, ry[1] + my, 7)

    x0, x1 = 46, l.ancho - 24
    y0, y1 = (46 if spec.get("titulo") else 24), l.alto - (46 if curvas and
                                                           len(curvas) > 1 else 30)
    px = lambda v: x0 + (v - xlo) / (xhi - xlo) * (x1 - x0)
    py = lambda v: y1 - (v - ylo) / (yhi - ylo) * (y1 - y0)

    for v in marcas_x:
        l.linea(px(v), y0, px(v), y1, color=REJILLA)
    for v in marcas_y:
        l.linea(x0, py(v), x1, py(v), color=REJILLA)

    ejex_y = py(0) if ylo <= 0 <= yhi else y1
    ejey_x = px(0) if xlo <= 0 <= xhi else x0
    l.flecha(x0, ejex_y, x1, ejex_y, grosor=1, cabeza=7)
    l.flecha(ejey_x, y1, ejey_x, y0, grosor=1, cabeza=7)
    l.texto(x1 - 2, ejex_y - 7, spec.get("nombre_x", "x"), tam=12, anclaje="rd")
    l.texto(ejey_x + 8, y0, spec.get("nombre_y", "y"), tam=12, anclaje="la")

    for v in marcas_x:
        if abs(v) > 1e-9:
            l.linea(px(v), ejex_y - 3, px(v), ejex_y + 3, color=TINTA)
            l.texto(px(v), ejex_y + 6, _fmt(v), tam=10, anclaje="ma", color=GRIS)
    for v in marcas_y:
        if abs(v) > 1e-9:
            l.linea(ejey_x - 3, py(v), ejey_x + 3, py(v), color=TINTA)
            l.texto(ejey_x - 6, py(v), _fmt(v), tam=10, anclaje="rm", color=GRIS)

    for i, c in enumerate(curvas):
        col = PALETA[i % len(PALETA)]
        pts = [(px(x), py(y)) for x, y in c["puntos"]]
        for a, b in zip(pts, pts[1:]):
            l.linea(*a, *b, color=col, grosor=2)
    for p in marcados:
        l.punto(px(p["x"]), py(p["y"]), r=4)
        if p.get("etiqueta"):
            l.texto(px(p["x"]) + 7, py(p["y"]) - 7, p["etiqueta"], tam=11, anclaje="ld")

    if len(curvas) > 1:
        x, y = x0, l.alto - 22
        for i, c in enumerate(curvas):
            col = PALETA[i % len(PALETA)]
            l.linea(x, y, x + 20, y, color=col, grosor=2)
            nom = c.get("nombre", "")
            l.texto(x + 26, y, nom, tam=11, anclaje="lm")
            x += 26 + l.medir(nom, 11)[0] + 20
    return l


def _borde(cx, cy, w, h, ang, holgura=0.0):
    """Punto donde el rayo que sale de (cx, cy) con ángulo `ang` cruza la caja."""
    hw, hh = w / 2 + holgura, h / 2 + holgura
    c, sn = math.cos(ang), math.sin(ang)
    t = min(hw / abs(c) if abs(c) > 1e-9 else float("inf"),
            hh / abs(sn) if abs(sn) > 1e-9 else float("inf"))
    return cx + t * c, cy + t * sn


def dibujar_esquema(spec: dict) -> Lienzo:
    nodos = spec.get("nodos") or []
    if not nodos:
        raise ErrorSpec("'esquema' necesita 'nodos'.")

    l = Lienzo(spec.get("ancho", 620), spec.get("alto", 400))
    if spec.get("titulo"):
        l.texto(l.ancho / 2, 16, spec["titulo"], tam=15, anclaje="ma", negrita=True)

    cajas, arriba = {}, 44 if spec.get("titulo") else 20
    ancho_caja = spec.get("ancho_nodo", 118)
    alto_caja = spec.get("alto_nodo", 52)
    for n in nodos:
        cx = 20 + n["x"] * (l.ancho - 40 - ancho_caja) + ancho_caja / 2
        cy = arriba + n["y"] * (l.alto - arriba - 20 - alto_caja) + alto_caja / 2
        cajas[n["id"]] = (cx, cy, ancho_caja, alto_caja)

    for n in nodos:
        cx, cy, w, h = cajas[n["id"]]
        if n.get("forma") == "elipse":
            l.elipse(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2,
                     relleno=(246, 246, 246), grosor=2)
        else:
            l.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2,
                   relleno=(246, 246, 246), grosor=2)
        lineas = _envolver(l, n["texto"], w - 14, 12)
        for j, ln in enumerate(lineas):
            l.texto(cx, cy - (len(lineas) - 1) * 7 + j * 14, ln, tam=12, anclaje="mm")

    for f in spec.get("flechas", []):
        for extremo in ("de", "a"):
            if f[extremo] not in cajas:
                raise ErrorSpec(f"la flecha apunta a un nodo inexistente: '{f[extremo]}'")
        (x1, y1, w1, h1) = cajas[f["de"]]
        (x2, y2, w2, h2) = cajas[f["a"]]
        ang = math.atan2(y2 - y1, x2 - x1)
        ax, ay = _borde(x1, y1, w1, h1, ang, 5)
        bx, by = _borde(x2, y2, w2, h2, ang + math.pi, 9)
        l.flecha(ax, ay, bx, by, grosor=2)
        if f.get("etiqueta"):
            # Desplazada perpendicular a la flecha, no hacia arriba: en una
            # flecha diagonal, "arriba" cae justo sobre la línea y la tacha.
            perp_x, perp_y = -math.sin(ang), math.cos(ang)
            if perp_y > 0:  # siempre hacia el lado de arriba
                perp_x, perp_y = -perp_x, -perp_y
            l.texto((ax + bx) / 2 + perp_x * 18, (ay + by) / 2 + perp_y * 18,
                    f["etiqueta"], tam=11, anclaje="mm", color=GRIS)

    return l


def dibujar_aviso(spec: dict) -> Lienzo:
    lineas = spec.get("lineas") or []
    if not lineas:
        raise ErrorSpec("'aviso' necesita 'lineas'.")

    l = Lienzo(spec.get("ancho", 420), spec.get("alto", 240))
    l.rect(6, 6, l.ancho - 6, l.alto - 6, relleno=(252, 252, 250), grosor=3)
    l.rect(16, 16, l.ancho - 16, l.alto - 16, relleno=None, borde=GRIS, grosor=1)

    tams = spec.get("tamanos") or [22 if i == 0 else 15 for i in range(len(lineas))]
    envueltas = []
    for txt, tam in zip(lineas, tams):
        for ln in _envolver(l, txt, l.ancho - 60, tam):
            envueltas.append((ln, tam))
    alto_total = sum(t * 1.5 for _, t in envueltas)
    y = (l.alto - alto_total) / 2
    for ln, tam in envueltas:
        l.texto(l.ancho / 2, y + tam * 0.75, ln, tam=tam, anclaje="mm",
                negrita=(tam >= 18))
        y += tam * 1.5
    return l


DIBUJANTES = {
    "barras": dibujar_barras,
    "lineas": dibujar_lineas,
    "dispersion": dibujar_dispersion,
    "torta": dibujar_torta,
    "cartesiano": dibujar_cartesiano,
    "esquema": dibujar_esquema,
    "aviso": dibujar_aviso,
}


def generar(spec: dict, salida: Path) -> Path:
    tipo = spec.get("tipo")
    if tipo not in DIBUJANTES:
        raise ErrorSpec(
            f"tipo '{tipo}' desconocido. Usa uno de: {', '.join(sorted(DIBUJANTES))}."
        )
    salida.parent.mkdir(parents=True, exist_ok=True)
    DIBUJANTES[tipo](spec).guardar(salida)
    return salida


def main(argv: list[str]) -> int:
    if len(argv) == 4 and argv[1] == "--lote":
        entrada, destino = Path(argv[2]), Path(argv[3])
        specs = sorted(entrada.glob("*.json"))
        if not specs:
            print(f"error: no hay .json en {entrada}", file=sys.stderr)
            return 1
        for s in specs:
            spec = json.loads(s.read_text(encoding="utf-8"))
            ruta = generar(spec, destino / f"{s.stem}.png")
            print(f"✓ {ruta}")
        return 0
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    print(f"✓ {generar(spec, Path(argv[2]))}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except ErrorSpec as e:
        print(f"error de especificación: {e}", file=sys.stderr)
        sys.exit(1)
