# Reglas ICFES para construir ítems

Fuente: `Base_MD/Manual_construccion_items_ICFES_2009.md` (Manual para la
construcción de ítems tipo selección de respuesta, C1.1.M01) y
`Base_MD/Guia_introductoria_diseno_centrado_evidencias.md`.

Estas reglas son el filtro de calidad. Aplícalas **antes** de escribir el JSON
y revísalas otra vez al final, pregunta por pregunta.

## Anatomía de un ítem

Todo ítem Saber 11.° es **selección múltiple con única respuesta (S.M.U.R.)**
y tiene tres partes:

| Parte | Definición del manual | Campo del formato |
|---|---|---|
| **Contexto** | La información necesaria para resolver la problemática: un texto, una gráfica, un dibujo, una tabla. Puede omitirse cuando el marco de referencia del objeto evaluado ya lo provee. | `contexto` (array de bloques) |
| **Enunciado** | El planteamiento de la problemática: **la tarea de evaluación**. Debe dar una idea completa y clara de qué se pide, con información necesaria y suficiente. | `enunciado` (array de bloques) |
| **Opciones** | Cuatro posibles respuestas. Solo una es válida (**clave**); las otras tres son **no válidas pero plausibles** para quien no domina la tarea. | `opciones` (4 objetos) |

Una opción no válida puede ser un error común, o una afirmación verdadera que
no responde completamente la pregunta.

> «La opción que responde correctamente (clave) debe diferenciarse de las demás
> **por su contenido y no por sutilezas del lenguaje**.»

## Diseño Centrado en Evidencias

La cadena que fija el estándar no es decorativa; es el método con que el ICFES
construye cada ítem:

**Competencia** (habilidad para aplicar conocimientos en contexto)
→ **Afirmación** (lo específico que se espera que el evaluado sepa hacer)
→ **Evidencia** (el aspecto observable que permite inferir la afirmación)
→ **Tarea de evaluación** (lo que el ítem le pide hacer al evaluado).

Escribe en este orden: primero eliges evidencia, después diseñas la tarea que
la hace observable, y solo entonces redactas contexto, enunciado y opciones.
Si al terminar el ítem la respuesta correcta se puede acertar sin ejercer la
evidencia declarada, el ítem no sirve aunque «se vea bien».

## Reglas generales

- Usar lenguaje claro, preciso y directo; minimizar el tiempo de lectura.
- Sin errores gramaticales, de puntuación, de ortografía ni de abreviaturas.
- Balancear la dificultad: el conjunto debe tener ítems de dificultad alta,
  media y baja.

## Reglas sobre el contenido

- **Una sola problemática por ítem.**
- Cada ítem debe corresponder a una tarea de evaluación definida en la
  estructura de prueba (es decir: a una evidencia real de la tabla del área).
- Cada ítem es **independiente**: no puede dar información que sirva para
  responder otro.
- Evitar: contenido trivial, información irrelevante, información ambigua en
  las opciones, discriminación muy fina entre opciones, y presentar principios
  de una forma distinta a como se aprenden en el colegio.
- Evitar evaluar el mismo aspecto específico con varios ítems.
- Evitar conocimientos muy específicos y vocabulario fuera del alcance de la
  población objetivo.
- Prohibido: ítems con posiciones ideológicas o prejuicios; ítems que indaguen
  por la **opinión** del evaluado; ítems cuya clave dependa de la opinión de
  quien lo construyó.
- Ítems **originales**: no partir de preguntas publicadas en internet, libros
  o revistas.

## Reglas sobre el enunciado

- **Sin nombres propios.** Ni personas, ni empresas, ni municipios, ni
  departamentos. En su lugar: «una paciente…», «un hospital universitario…»,
  «un almacén de telas…», «un municipio del norte del país…».
- Las directrices deben ser claras: se debe reconocer sin ambigüedad qué se
  está preguntando.
- Evitar textos excesivos.
- Redactar en positivo. Si la negación es indispensable, va en **MAYÚSCULA Y
  NEGRITA**: `NO`, `EXCEPTO`.

## Reglas sobre las opciones

- **Exactamente cuatro opciones** (A, B, C, D). Es la decisión del ICFES.
  El formato admite un mínimo de 2 para otros usos, pero un paquete Saber 11.°
  usa 4 — salvo las partes 2 a 5 de Inglés, que usan 3 por diseño oficial.
- Concordancia gramatical de cada opción con el enunciado.
- Todas las opciones se refieren al mismo contenido y son **independientes
  entre sí**: no se solapan, no se intersectan, no son sinónimas.
- Longitud similar, al menos por pares.
- Opciones numéricas ordenadas de menor a mayor (o al revés) de forma
  consistente en todo el paquete.
- Redactadas en positivo.
- No repetir en las opciones frases o palabras significativas del enunciado.
- Evitar adverbios absolutos: *siempre, nunca, totalmente, absolutamente,
  completamente*.
- **Nunca** usar «Todas las anteriores», «Ninguna de las anteriores» ni «A y B
  son correctas».
- Evitar opciones fácilmente descartables por obvias.
- Equilibrar la posición de la clave: A, B, C y D deben aparecer en
  proporciones parecidas en el paquete completo.

### La clave no debe delatarse

El manual lista los seis modos en que la clave se hace reconocible sin saber
la respuesta. Revísalos uno por uno en cada ítem:

1. Ser la más larga o la más corta.
2. Ser la más precisa o la más imprecisa.
3. Estar redactada en un registro distinto (técnico frente a común).
4. Tener el mayor nivel de generalización o de particularización.
5. Repetir palabras del enunciado.
6. Ser la única gramaticalmente concordante con el enunciado.

### Justificaciones

El manual exige justificar **cada una** de las cuatro opciones, no solo la
clave: es lo que garantiza que hay una sola respuesta válida y que las otras
tres son plausibles. El formato lo vuelve obligatorio (`justificacion` por
opción).

Escribe cada justificación así:

- **Clave:** empieza por `Correcta:` y explica el razonamiento que lleva a
  ella, apoyado en el estímulo. No basta con repetir la opción.
- **Distractores:** empieza por `Incorrecta:` y nombra **el error específico**
  que comete quien la elige (qué dato leyó mal, qué concepto confundió, qué
  paso del procedimiento invirtió). Una justificación que solo dice «no es la
  respuesta correcta» está mal escrita.

## Niveles de dificultad

Cada ítem debe caer en un nivel deliberado, no por accidente:

- **Baja** — la evidencia se ejerce en un paso, sobre información explícita
  en el estímulo.
- **Media** — exige relacionar dos o más piezas del estímulo, o un
  procedimiento de varios pasos.
- **Alta** — exige integrar el estímulo con conocimiento del área, evaluar la
  validez de algo, o descartar distractores muy plausibles.

El estándar `preguntas-icfes` v1 no tiene campo de dificultad (está listado
como extensión futura). Deja constancia del nivel en `que_evalua` si importa:
`"que_evalua": "Dificultad media. Interpretación de una gráfica de barras
para comparar dos periodos."`

## Lista de verificación final

Antes de empaquetar, revisa cada ítem contra esto:

- [ ] La clave es inequívocamente correcta y las otras tres inequívocamente incorrectas.
- [ ] Un experto del área no discutiría la clave.
- [ ] Toda la información necesaria está en el estímulo o es del currículo de la media.
- [ ] La evidencia declarada es la que realmente se ejerce al responder.
- [ ] Ninguna de las seis formas de delatar la clave está presente.
- [ ] Las cuatro justificaciones nombran razones distintas y específicas.
- [ ] Sin nombres propios, sin opiniones, sin ideología, sin «todas las anteriores».
- [ ] La posición de la clave está equilibrada en el paquete completo.
- [ ] Si hay imagen, la pregunta **no se puede responder sin verla**, y la
      `descripcion_accesible` describe lo que se ve sin revelar la respuesta.
