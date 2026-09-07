# El formato de salida: un archivo JSON por pregunta

Contrato de datos completo:
<https://github.com/Riskbreaker2077/preguntas-icfes>
(especificación en `docs/especificacion.md`, esquemas en `schema/v1/`).

Cada pregunta se guarda en **su propio archivo**, con la forma que define
`schema/v1/pregunta.schema.json`. Es la misma organización del banco
[`banco-preguntas-icfes`](https://github.com/Riskbreaker2077/banco-preguntas-icfes),
de modo que el ZIP que produce la skill se descomprime encima de un banco
existente sin tocar nada más.

## Estructura de la salida

```
salida/<nombre>/            ← carpeta de trabajo
├── _specs/                 ← especificaciones de las imágenes (no entra al ZIP)
└── banco/                  ← esto es lo único que se empaqueta
    └── ciencias-sociales/
        ├── cs-155.json     ← una pregunta por archivo, el nombre es su id
        ├── cs-156.json
        ├── grupos/
        │   └── cs-g-002.json
        ├── imagenes/
        │   └── cs-170-1.png
        └── fuentes/
            └── cuadernillo-2024.pdf
```

| Ruta | Qué va ahí |
|---|---|
| `<area>/<id>.json` | Una pregunta. **El nombre del archivo es su `id`**; el empaquetador lo exige. |
| `<area>/grupos/<id>.json` | Un grupo, con id de la forma `<prefijo>-g-NNN`. |
| `<area>/imagenes/<id>-N.png` | Prefijadas con el id de la pregunta **o del grupo** que las usa, para que nunca colisionen. `.png`, `.jpg`, `.jpeg` o `.webp`. |
| `<area>/fuentes/<slug>.pdf` | El PDF de origen, cuando la pregunta declara `fuentes`. Se comparte entre las preguntas del mismo PDF. |

### Áreas y prefijos de id

| Área | Carpeta | Prefijo |
|---|---|---|
| Matemáticas | `matematicas/` | `mt` |
| Lectura Crítica | `lenguaje/` | `lg` |
| Sociales y Ciudadanas | `ciencias-sociales/` | `cs` |
| Ciencias Naturales | `ciencias-naturales/` | `cn` |
| Inglés | `ingles/` | `in` |

Los ids se numeran con tres dígitos y son consecutivos dentro del área.
`scripts/siguiente_id.py` da el próximo libre sin que tengas que mirar la
carpeta:

```bash
python3 scripts/siguiente_id.py <area> --cuantos 20
python3 scripts/siguiente_id.py <area> --grupo
```

## No hay `paquete.json`

El banco guarda preguntas sueltas; el paquete envolvente es otra cosa, que
se ensambla al exportar hacia una plataforma. Por eso **cada pregunta declara
su propio `version_estandar`**: fuera de un paquete, el archivo no tiene
ninguna otra forma de decir qué versión del estándar necesita quien lo lea.

No es la versión con la que se escribió, sino la mínima que exigen los campos
que la pregunta realmente usa:

| Si la pregunta usa… | `version_estandar` mínimo |
|---|---|
| solo los campos básicos | `1.0.0` |
| `grado`, `prueba`, `procedencia`, `verificado` o `fuentes` | `1.1.0` |
| `grupo_id`, `tipo_item`, `nivel_mcer`, `valor`, o un número de opciones distinto de 4 | `1.2.0` |

`scripts/empaquetar.py` avisa si falta, y el validador rechaza la pregunta si
lo declarado es menor que lo que exigen sus campos. `scripts/banco.py` calcula
el valor correcto con `version_minima()`.

## Cómo se valida

El estándar valida **paquetes**, no archivos sueltos. Para validar un banco,
`scripts/empaquetar.py` envuelve cada área en un paquete sintético y se lo
pasa al validador de referencia — la misma técnica de `validar-banco.mjs` en
el repo del banco. Las 13 invariantes se comprueban igual, incluidas las
referencias cruzadas entre preguntas, grupos e imágenes.

```bash
python3 scripts/empaquetar.py salida/<nombre> --solo-validar
python3 scripts/empaquetar.py salida/<nombre> -o entrega/paquete.zip
```

## Integrarse a un banco existente

Antes de escribir nada, **mira qué vocabulario usa ya el área de destino** y
cópialo. El valor del formato está en que un consumidor agrupe por cadena
exacta, así que dos redacciones de la misma competencia rompen justo lo que
el banco intenta ganar.

```bash
python3 -c "import json,glob,collections;\
qs=[json.load(open(f)) for f in glob.glob('banco/ciencias-sociales/*.json')];\
print(collections.Counter(q.get('componente') for q in qs))"
```

Lo que hay hoy en `banco-preguntas-icfes` viene de cuadernillos de **Evaluar
para Avanzar**, así que usa el vocabulario de esa prueba y no el de Saber
11.°:

| Área del banco | `componente` en uso |
|---|---|
| `ciencias-sociales` | Sujeto, sociedad y Estado · Participación y responsabilidad democrática · Ambiente y desarrollo · Pluralidad, identidad y valoración de las diferencias · Convivencia y paz · Historia y cultura |
| `ciencias-naturales` | Entorno vivo · Entorno físico · Procesos vivos · Procesos físicos · Procesos químicos · Ciencia, tecnología y sociedad |
| `ingles` | *(ninguno: la metadata vive en el grupo, y las preguntas solo declaran `nivel_mcer`)* |

Además, el banco escribe `competencia` en **Title Case** («Pensamiento
Social») y `afirmacion`/`evidencia` **sin el número** que las encabeza en las
tablas oficiales.

Las referencias por área de esta skill traen, en cambio, el vocabulario
**literal de Saber 11.°**, que es el correcto para un paquete autónomo. Si el
encargo es alimentar el banco, pregunta cuál de los dos usar: no son
intercambiables y la elección cambia los veinte archivos.

## Una pregunta estándar

```json
{
  "id": "mt-001",
  "version_estandar": "1.1.0",
  "competencia": "Interpretación y representación",
  "componente": "Estadística",
  "afirmacion": "Comprende y transforma la información cuantitativa y esquemática presentada en distintos formatos.",
  "evidencia": "1.1 Da cuenta de las características básicas de la información presentada en diferentes formatos, como series, gráficas, tablas y esquemas.",
  "estandar_asociado": "Interpreto y comparo resultados de estudios con información estadística provenientes de medios de comunicación.",
  "que_evalua": "La lectura de una gráfica de barras agrupadas para comparar dos cuencas.",
  "grado": "11",
  "prueba": "saber11",
  "valor": 1,
  "procedencia": {
    "contenido": "ia_generada",
    "clasificacion": "ia_generada",
    "respuesta_correcta": "ia_generada"
  },
  "verificado": { "contenido": false, "clasificacion": false, "respuesta_correcta": false },
  "contexto": [
    { "tipo": "texto", "texto": "La gráfica muestra el consumo de agua…" },
    { "tipo": "imagen", "archivo": "mt-001-1.png",
      "descripcion_accesible": "Gráfica de barras agrupadas con cuatro sectores y dos cuencas." }
  ],
  "enunciado": [
    { "tipo": "texto", "texto": "De acuerdo con la gráfica, ¿en cuál sector la diferencia entre las dos cuencas es mayor?" }
  ],
  "opciones": [
    { "id": "A", "contenido": [{ "tipo": "texto", "texto": "Agrícola" }],
      "es_correcta": true,
      "justificacion": "Correcta: 120 − 95 = 25 millones de m³, la mayor de las cuatro diferencias." },
    { "id": "B", "contenido": [{ "tipo": "texto", "texto": "Industrial" }],
      "es_correcta": false,
      "justificacion": "Incorrecta: la diferencia es 17 millones de m³. Quien la elige se fija en la barra que más crece de una cuenca a otra, no en la diferencia absoluta." }
  ]
}
```

### Campos de una pregunta

**Los 6 de metadata pedagógica** — obligatorios, propios o heredados de un
grupo: `competencia`, `componente`, `afirmacion`, `evidencia`,
`estandar_asociado`, `que_evalua`. Los cinco primeros salen **literalmente**
de la referencia del área; `que_evalua` es texto libre, lo escribes tú.

**Estructurales** — `id` (único, estable), `contexto` (array, puede ir vacío),
`enunciado` (mínimo 1 bloque), `opciones` (mínimo 2; en Saber 11.°, cuatro).

**Opcionales útiles** — `grado` (`"3"`…`"11"`), `prueba` (`"saber11"` o
`"evaluar_para_avanzar"`), `valor` (peso, >0, por defecto 1), `nivel_mcer`
(`"Pre A1"`…`"C2"`, solo Inglés), `grupo_id`, `tipo_item`.

**Trazabilidad** — `procedencia`, `verificado` y `fuentes`, cada uno con las
tres claves `contenido`, `clasificacion` y `respuesta_correcta`.
`procedencia` toma `"oficial"`, `"extraido_oficial"` o `"ia_generada"`.
Una opción puede además llevar `procedencia_justificacion` y
`justificacion_verificada` propias.

> **Regla de honestidad de esta skill.** Todo lo que genera la skill es
> `"ia_generada"` y `verificado: false` en los tres bloques. Nada se marca
> como `"oficial"` salvo que venga transcrito de un documento del ICFES, y en
> ese caso el PDF va en `fuentes/` y se nombra en `fuentes`. Marcar
> `verificado: true` es potestad de la persona que revisó la pregunta, nunca
> de la skill.

### Opciones

Cada una: `id` (`"A"`…`"D"`), `contenido` (array de bloques, mínimo 1),
`es_correcta` (booleano; **exactamente una** en `true`) y `justificacion`
(específica de esa opción, nunca una explicación general compartida).

## Bloques de contenido

`contexto`, `enunciado` y el `contenido` de cada opción son **arrays de
bloques**, así que una misma pregunta mezcla párrafo, imagen y tabla en el
orden que haga falta.

```json
{ "tipo": "texto", "texto": "…" }

{ "tipo": "imagen", "archivo": "cs-155-1.png",
  "descripcion_accesible": "…" }

{ "tipo": "tabla",
  "encabezados": ["Grupo etario", "Participación (%)"],
  "filas": [["18-28 años", "42"], ["29-45 años", "58"]] }
```

- `archivo` es solo el nombre, sin carpeta, y debe existir en `<area>/imagenes/`
  con la forma `<id>-N.ext`, donde `<id>` es el de la pregunta o del grupo que lo usa.
- Toda fila de una tabla tiene tantas celdas como encabezados. Todas las celdas son *strings*.
- **Si el estímulo es tabular, usa el bloque `tabla`, no una imagen de tabla.**

## Grupos

Un grupo es el mecanismo para que varias preguntas compartan un estímulo sin
duplicarlo. Vive en su propio archivo, `<area>/grupos/<prefijo>-g-NNN.json`,
y cada miembro lo referencia por `grupo_id`. Tres tipos:

### `contexto_compartido`

Un texto, caso o gráfica que sostiene varias preguntas — el caso normal en
Lectura Crítica, Sociales y las partes 5 y 6 de Inglés.

`lenguaje/grupos/lg-g-001.json`:

```json
{
  "id": "lg-g-001",
  "tipo": "contexto_compartido",
  "contexto": [{ "tipo": "texto", "texto": "«El oficio de vivir»…" }],
  "metadata_pedagogica": {
    "competencia": "Competencia lectora", "componente": "Texto continuo literario",
    "afirmacion": "…", "evidencia": "…", "estandar_asociado": "…", "que_evalua": "…"
  },
  "procedencia_contenido": "ia_generada",
  "verificado_contenido": false
}
```

Cada miembro lleva `"grupo_id": "lg-g-001"`, su `enunciado` y sus
`opciones`; `tipo_item` se omite o vale `"estandar"`. Si el grupo declara
`metadata_pedagogica`, los miembros que no traigan la suya la heredan — útil
cuando todas comparten componente y afirmación, y cada una difiere solo en
`evidencia`, que entonces sí conviene poner en la pregunta.

### `banco_opciones`

Emparejamiento: N descripciones contra un banco común de opciones — la parte 1
de Inglés.

`ingles/grupos/in-g-001.json`:

```json
{ "id": "in-g-001", "tipo": "banco_opciones",
  "contexto": [{ "tipo": "texto", "texto": "Match each description with a word." }],
  "banco": [
    { "id": "A", "contenido": [{ "tipo": "texto", "texto": "glasses" }] },
    { "id": "H", "contenido": [{ "tipo": "texto", "texto": "hat" }], "es_ejemplo": true }
  ] }
```

Cada miembro: `"tipo_item": "miembro_banco_opciones"`, `grupo_id`, `enunciado`
(la descripción), `respuesta_pool_id` (un `id` del banco que **no** sea el
`es_ejemplo`) y una `justificacion` propia. **No lleva `opciones`.**

### `texto_con_blancos`

*Cloze*: un pasaje con espacios numerados — partes 4 y 7 de Inglés.

`ingles/grupos/in-g-002.json`:

```json
{ "id": "in-g-002", "tipo": "texto_con_blancos",
  "contexto": [{ "tipo": "texto",
    "texto": "Last summer I (16)_______ to the coast with my family." }] }
```

Cada miembro: `"tipo_item": "miembro_texto_con_blancos"`, `grupo_id`,
`numero_blanco` (entero ≥ 1, único dentro del grupo) y sus `opciones`.
**No lleva `enunciado`.**

Los números del pasaje son tipografía, no estructura: el estándar no los
interpreta. Si el número debe seguir a la pregunta cuando cambia de posición
en el examen, usa el marcador dinámico (abajo) en vez del número fijo.

### Peso de un grupo

Un grupo de N preguntas vale N puntos, no 1. Si usas `valor`, ponlo por
pregunta; nunca cuentes el grupo como una sola.

## Numeración dinámica

Dentro de cualquier bloque `texto` puedes escribir `{{numero:id-de-pregunta}}`
y la plataforma consumidora lo sustituye por el número que esa pregunta tenga
en el examen concreto del estudiante:

```json
{ "tipo": "texto",
  "texto": "Last summer I ({{numero:in-016}})_______ to the coast." }
```

El `id` referenciado debe existir como archivo de pregunta en la misma área.
No hay escape para `{{` literal.

## Invariantes que se validan

Un solo error rechaza el área completa. `scripts/empaquetar.py` las corre
todas, área por área, antes de escribir el ZIP:

1. Cada pregunta con `opciones` tiene al menos 2 y **exactamente una** correcta. Una `miembro_banco_opciones` no lleva opciones; su `respuesta_pool_id` existe en el banco y no es la entrada de ejemplo.
2. Toda opción tiene `justificacion` no vacía, incluidas las incorrectas.
3. Los 6 campos de metadata están presentes y no vacíos, propios o heredados.
4. Toda imagen referenciada existe en `imagenes/`.
5. Toda tabla tiene filas rectangulares.
6. `id` de pregunta y `id` de grupo únicos dentro del paquete.
7. `estandar` es exactamente `"preguntas-icfes"` y `version_estandar` es SemVer.
8. Todo archivo de `fuentes.*` existe en `fuentes/`.
9. `grupo_id` existe y `tipo_item` concuerda con el `tipo` del grupo.
10. `numero_blanco` único dentro de su grupo.
11. `nivel_mcer` del catálogo MCER; `valor` mayor que 0.
12. `version_estandar` de una pregunta (si está) ≥ la que exigen sus campos.
13. Todo `{{numero:ID}}` referencia un `id` de pregunta existente en el área.

A lo que añade `scripts/empaquetar.py`, propio del banco: el nombre de cada
archivo coincide con el `id` que declara, y cada imagen se llama `<id>-N.ext`
con el id de la pregunta o grupo que la usa.
