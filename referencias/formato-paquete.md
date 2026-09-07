# El formato de salida: `preguntas-icfes`

Contrato de datos completo:
<https://github.com/Riskbreaker2077/preguntas-icfes>
(especificación en `docs/especificacion.md`, esquemas en `schema/v1/`).

Esta skill produce paquetes de la **versión 1.4.0** del estándar y los valida
con la implementación de referencia vendorizada en `scripts/vendor/validar.js`.

## Estructura del ZIP

```
paquete.zip
├── paquete.json      ← obligatorio
├── imagenes/         ← solo si hay bloques de tipo imagen
│   └── grafica-consumo.png
└── fuentes/          ← solo si alguna pregunta declara "fuentes"
    └── cuadernillo-2024.pdf
```

Extensiones admitidas: `.png`, `.jpg`, `.jpeg`, `.webp` en `imagenes/`;
`.pdf` en `fuentes/`. Nada más entra al ZIP.

## El paquete

```json
{
  "estandar": "preguntas-icfes",
  "version_estandar": "1.4.0",
  "nombre": "Saber 11.° · Matemáticas · Estadística (10 preguntas)",
  "area": "Matemáticas",
  "grupos": [],
  "preguntas": []
}
```

| Campo | Obligatorio | Qué es |
|---|---|---|
| `estandar` | sí | Literal `"preguntas-icfes"`. |
| `version_estandar` | sí | SemVer. Usa `"1.4.0"`. |
| `nombre` | sí | Nombre legible del paquete. |
| `area` | no | Área o asignatura, texto libre. |
| `preguntas` | sí | Mínimo 1. Los `id` son únicos en el paquete. |
| `grupos` | no | Preguntas que comparten estímulo. `id` únicos. |

No se admite ningún otro campo de primer nivel.

## Una pregunta estándar

```json
{
  "id": "mat-est-001",
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
    { "tipo": "imagen", "archivo": "grafica-consumo.png",
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

{ "tipo": "imagen", "archivo": "grafica.png",
  "descripcion_accesible": "…" }

{ "tipo": "tabla",
  "encabezados": ["Grupo etario", "Participación (%)"],
  "filas": [["18-28 años", "42"], ["29-45 años", "58"]] }
```

- `archivo` es solo el nombre, sin carpeta, y el archivo debe existir en `imagenes/`.
- Toda fila de una tabla tiene tantas celdas como encabezados. Todas las celdas son *strings*.
- **Si el estímulo es tabular, usa el bloque `tabla`, no una imagen de tabla.**

## Grupos

Un grupo es el mecanismo para que varias preguntas compartan un estímulo sin
duplicarlo. Tres tipos:

### `contexto_compartido`

Un texto, caso o gráfica que sostiene varias preguntas — el caso normal en
Lectura Crítica, Sociales y las partes 5 y 6 de Inglés.

```json
"grupos": [{
  "id": "lc-texto-01",
  "tipo": "contexto_compartido",
  "contexto": [{ "tipo": "texto", "texto": "«El oficio de vivir»…" }],
  "metadata_pedagogica": {
    "competencia": "Competencia lectora", "componente": "Texto continuo literario",
    "afirmacion": "…", "evidencia": "…", "estandar_asociado": "…", "que_evalua": "…"
  }
}]
```

Cada miembro lleva `"grupo_id": "lc-texto-01"`, su `enunciado` y sus
`opciones`; `tipo_item` se omite o vale `"estandar"`. Si el grupo declara
`metadata_pedagogica`, los miembros que no traigan la suya la heredan — útil
cuando todas comparten componente y afirmación, y cada una difiere solo en
`evidencia`, que entonces sí conviene poner en la pregunta.

### `banco_opciones`

Emparejamiento: N descripciones contra un banco común de opciones — la parte 1
de Inglés.

```json
{ "id": "en-p1-01", "tipo": "banco_opciones",
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

```json
{ "id": "en-p4-01", "tipo": "texto_con_blancos",
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
  "texto": "Last summer I ({{numero:en-p4-016}})_______ to the coast." }
```

El `id` referenciado debe existir en `paquete.preguntas`. No hay escape para
`{{` literal.

## Invariantes que se validan

Un solo error rechaza el paquete completo. `scripts/empaquetar.py` las corre
todas antes de escribir el ZIP:

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
13. Todo `{{numero:ID}}` referencia un `id` existente.
