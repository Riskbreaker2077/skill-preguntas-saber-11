# Preguntas con imagen

Una pregunta de imagen + texto es una pregunta normal con un bloque
`{"tipo": "imagen", ...}` dentro de `contexto` (lo habitual), de `enunciado` o
del `contenido` de una opción.

## Antes de generar nada: ¿de verdad va imagen?

- **Si el estímulo es tabular → bloque `tabla`, no imagen.** El bloque nativo
  se lee con lector de pantalla, se busca por texto y no se pixela.
- **La imagen debe ser necesaria.** Si la pregunta se responde sin mirarla, es
  decoración: quítala. Es la última casilla de la lista de verificación de
  `construccion-items.md`.
- **La imagen no puede contener la respuesta escrita.** Que ilustre el
  fenómeno, no que lo rotule.

## El flujo

```bash
# 1. escribes la especificación de la imagen
cat > salida/mi-paquete/_specs/grafica-consumo.json

# 2. la generas
python3 scripts/imagen.py salida/mi-paquete/_specs/grafica-consumo.json \
                          salida/mi-paquete/imagenes/grafica-consumo.png

# o todas de una vez
python3 scripts/imagen.py --lote salida/mi-paquete/_specs salida/mi-paquete/imagenes

# 3. la referencias en la pregunta
#    { "tipo": "imagen", "archivo": "grafica-consumo.png",
#      "descripcion_accesible": "…" }
```

Guarda las especificaciones en `_specs/` dentro de la carpeta de trabajo:
`empaquetar.py` no las mete al ZIP (solo avisa), y quedan como fuente
editable de cada imagen.

Nombres de archivo en minúsculas, con guiones, descriptivos:
`grafica-consumo-agua.png`, no `img1.png`.

## `descripcion_accesible`

Obligatoria en la práctica (el empaquetador avisa si falta). Describe **lo que
se ve**, con el detalle suficiente para responder sin ver la imagen, y sin
delatar la clave:

> ✅ «Gráfica de barras agrupadas: consumo de agua en millones de m³ para
> cuatro sectores (agrícola, industrial, doméstico y servicios) en dos
> cuencas. Cuenca alta: 120, 45, 80, 30. Cuenca baja: 95, 62, 55, 41.»
>
> ❌ «Gráfica que muestra que el sector agrícola tiene la mayor diferencia.»
> (delata la respuesta)
>
> ❌ «Una gráfica de barras.» (no permite responder)

## Los siete tipos

Todos aceptan `titulo` (opcional), y `ancho` y `alto` en píxeles para
sobrescribir el tamaño por defecto. El dibujo se hace a 2× y se reduce, así
que las líneas y el texto salen suavizados.

### `barras` — comparar categorías · 620×400

Una o varias series. Con dos o más aparece la leyenda automáticamente.

```json
{
  "tipo": "barras",
  "titulo": "Consumo de agua por sector (2024)",
  "eje_x": "Sector",
  "eje_y": "Millones de m³",
  "categorias": ["Agrícola", "Industrial", "Doméstico", "Servicios"],
  "series": [
    { "nombre": "Cuenca alta", "valores": [120, 45, 80, 30] },
    { "nombre": "Cuenca baja", "valores": [95, 62, 55, 41] }
  ],
  "mostrar_valores": true
}
```

Cada serie debe traer tantos `valores` como `categorias`. Con
`"mostrar_valores": false` se ocultan los números sobre las barras — úsalo
cuando la tarea sea *leer la gráfica*, no comparar cifras ya escritas.

### `lineas` — evolución en el tiempo · 620×400

Mismos campos que `barras`. Los puntos se unen en el orden de `categorias`.

```json
{ "tipo": "lineas", "titulo": "Temperatura promedio",
  "eje_x": "Mes", "eje_y": "°C",
  "categorias": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
  "series": [{ "nombre": "Estación A", "valores": [18.2, 19.1, 20.4, 21.0, 20.2, 18.9] }] }
```

### `dispersion` — relación entre dos variables · 620×420

El eje X es numérico. Con `series` dibuja varios conjuntos; con `puntos`, uno solo.

```json
{ "tipo": "dispersion", "titulo": "Masa y periodo del péndulo",
  "eje_x": "Masa (g)", "eje_y": "Periodo (s)",
  "series": [
    { "nombre": "Cuerda 40 cm", "puntos": [[10, 1.27], [20, 1.26], [30, 1.28]] },
    { "nombre": "Cuerda 80 cm", "puntos": [[10, 1.79], [20, 1.80], [30, 1.78]] }
  ] }
```

### `torta` — reparto de un total · 560×400

Los porcentajes se calculan solos; la leyenda va a la derecha con el valor
absoluto. Los segmentos por debajo del 6 % no llevan etiqueta dentro.

```json
{ "tipo": "torta", "titulo": "Residuos recolectados",
  "segmentos": [
    { "etiqueta": "Orgánicos", "valor": 48 },
    { "etiqueta": "Plásticos", "valor": 22 },
    { "etiqueta": "Papel y cartón", "valor": 17 }
  ] }
```

### `cartesiano` — funciones y puntos en el plano · 520×460

Ejes con flecha que pasan por el origen si el 0 entra en el rango. Muestrea la
función tú: pasa los puntos ya calculados.

```json
{ "tipo": "cartesiano", "titulo": "Trayectoria del proyectil",
  "nombre_x": "t (s)", "nombre_y": "h (m)",
  "rango_x": [-4, 4], "rango_y": [-3.5, 1.5],
  "curvas": [{ "nombre": "f(x) = x²/4 − 3",
               "puntos": [[-4, 1], [-3, -0.75], [-2, -2], [0, -3], [2, -2], [4, 1]] }],
  "puntos_marcados": [{ "x": 0, "y": -3, "etiqueta": "V(0, −3)" }] }
```

Con 30–60 puntos la curva sale suave. `rango_x` y `rango_y` son opcionales: sin
ellos se ajusta a los datos.

### `esquema` — diagramas de cajas y flechas · 620×400

Redes tróficas, procesos, ciclos, circuitos en bloques, mapas conceptuales.
`x` e `y` van de 0 a 1 (0,0 arriba a la izquierda), así que colocas los nodos
sin pensar en píxeles.

```json
{ "tipo": "esquema", "titulo": "Red trófica del humedal",
  "nodos": [
    { "id": "a", "texto": "Algas", "x": 0.0, "y": 0.5, "forma": "elipse" },
    { "id": "b", "texto": "Caracoles", "x": 0.33, "y": 0.1 },
    { "id": "c", "texto": "Larvas de insecto", "x": 0.33, "y": 0.9 },
    { "id": "d", "texto": "Peces pequeños", "x": 0.68, "y": 0.5 },
    { "id": "e", "texto": "Garza", "x": 1.0, "y": 0.5 }
  ],
  "flechas": [
    { "de": "a", "a": "b" }, { "de": "a", "a": "c" },
    { "de": "b", "a": "d" }, { "de": "c", "a": "d" },
    { "de": "d", "a": "e", "etiqueta": "depreda" }
  ] }
```

`forma` admite `"elipse"`; por defecto es rectángulo. `ancho_nodo` y
`alto_nodo` cambian el tamaño de todas las cajas (118×52 por defecto). El
texto se envuelve solo dentro de la caja.

### `aviso` — letreros y señales · 420×240

El caso de la parte 2 de Inglés, y de cualquier etiqueta o aviso publicitario
de un texto discontinuo en Lectura Crítica.

```json
{ "tipo": "aviso",
  "lineas": ["QUIET PLEASE", "Exams in progress", "Please leave your bags outside"] }
```

La primera línea sale grande y en negrita. `tamanos` permite fijar el tamaño
de cada línea, p. ej. `[26, 14, 14]`.

## Cuándo ninguno sirve

Si la pregunta necesita una fotografía, un mapa geográfico real, una caricatura
dibujada o una figura con geometría fina que ninguno de los siete tipos cubre:
**no la improvises con `esquema`**. Escoge una de estas dos salidas y dilo en
el informe de entrega:

1. Reformula la pregunta para que el estímulo sea uno que sí se puede generar
   (una gráfica, un diagrama, una tabla) sin perder la evidencia evaluada.
2. Deja la pregunta sin imagen y pide el archivo: quien lo aporte lo copia a
   `imagenes/` con el nombre que ya declara la pregunta, y `empaquetar.py`
   fallará hasta que exista.

Nunca entregues una imagen que aparente ser una fotografía, un mapa oficial o
un cuadernillo del ICFES sin serlo.
