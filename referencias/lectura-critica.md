# Lectura Crítica — taxonomía oficial Saber 11.°

Fuente: `Base_MD/Guia_orientacion_Saber11_2026-2.md` (§B) y
`Base_MD/Marco_referencia_lectura_critica_saber11.md`.

**Prueba real:** 41 preguntas, todas en la primera sesión.

## Competencia

La prueba evalúa **una sola competencia**: la *competencia lectora*. Por eso,
en todas las preguntas de esta área:

```json
"competencia": "Competencia lectora"
```

Lo que varía entre preguntas es la **afirmación** (el proceso cognitivo).

## Afirmaciones y evidencias

| Afirmación (proceso) | Evidencias |
|---|---|
| 1. Identifica y entiende los contenidos locales que conforman un texto. (25 %)<br>*Identificar y ubicar información local* | 1.1 Entiende el significado de los elementos locales que constituyen un texto.<br>1.2 Identifica los eventos narrados de manera explícita en un texto (literario, descriptivo, caricatura o cómic) y los personajes involucrados (si los hay). |
| 2. Comprende cómo se articulan las partes de un texto para darle un sentido global. (42 %)<br>*Relacionar e interpretar información* | 2.1 Comprende la estructura formal de un texto y la función de sus partes.<br>2.2 Identifica y caracteriza las diferentes voces o situaciones presentes en un texto.<br>2.3 Comprende las relaciones entre diferentes partes o enunciados de un texto.<br>2.4 Identifica y caracteriza las ideas o afirmaciones presentes en un texto informativo.<br>2.5 Identifica el tipo de relación existente entre diferentes elementos de un texto (discontinuo). |
| 3. Reflexiona a partir de un texto y evalúa su contenido. (33 %)<br>*Evaluar y reflexionar sobre la forma y el contenido* | 3.1 Establece la validez e implicaciones de un enunciado de un texto (argumentativo o expositivo).<br>3.2 Establece relaciones entre un texto y otros textos o enunciados.<br>3.3 Reconoce contenidos valorativos presentes en un texto.<br>3.4 Reconoce las estrategias discursivas en un texto.<br>3.5 Contextualiza adecuadamente un texto o la información contenida en este. |

La afirmación 1 responde a ¿qué?, ¿dónde?, ¿cuándo?, ¿quién?, ¿de qué manera?
La 2 exige articular varios elementos locales. La 3 es la propiamente crítica
y presupone las dos anteriores.

## Componente

`componente` registra el tipo de texto del estímulo. Valores:

| Formato | Literarios | Informativos (descriptivos, expositivos, argumentativos) |
|---|---|---|
| **Continuos** | Novela, cuento, poesía, canción, dramaturgia | Ensayo, columna de opinión, crónica |
| **Discontinuos** | Caricatura, cómic | Etiqueta, infografía, tabla, diagrama, aviso publicitario, manual, reglamento |

Escríbelo como `"Texto continuo literario"`, `"Texto continuo informativo
filosófico"`, `"Texto continuo informativo no filosófico"`, `"Texto
discontinuo literario"` o `"Texto discontinuo informativo"`, que son las
cinco categorías con que el ICFES reparte la prueba:

| Tipo de texto | % de preguntas |
|---|---|
| Continuo literario | 24 % |
| Continuo informativo filosófico | 30 % |
| Continuo informativo no filosófico | 30 % |
| Discontinuo literario | 8 % |
| Discontinuo informativo | 8 % |

## Estándar asociado

Cita un Estándar Básico de Competencias en Lenguaje (MEN), ciclo 10.º–11.º:

- «Comprendo e interpreto textos con actitud crítica y capacidad argumentativa.»
- «Analizo crítica y creativamente diferentes manifestaciones literarias del contexto universal.»
- «Interpreto en textos de la tradición oral y de la literatura los elementos que dan cuenta de una visión de mundo.»
- «Identifico, caracterizo y valoro diferentes grupos humanos teniendo en cuenta aspectos étnicos, lingüísticos, sociales y culturales.»
- «Comprendo el papel que cumplen los medios de comunicación masiva en el contexto social, cultural, económico y político de las sociedades.»

## Cómo se arma una pregunta de esta prueba

Un texto suele sostener **varias preguntas**. Eso es un grupo de tipo
`contexto_compartido`: el texto va una sola vez en `grupos[].contexto` y cada
pregunta miembro lleva su propio `enunciado` y sus opciones. Ver
`formato-paquete.md`, sección «Grupos».

Reglas propias del área:

- El texto del estímulo debe ser **original o de dominio público**, nunca un
  fragmento pegado de un libro con derechos. Si escribes el texto, escríbelo
  completo y coherente: no un resumen de otro texto.
- Extensión típica: 150–400 palabras para textos continuos.
- La pregunta no puede exigir conocimiento disciplinar externo al texto: se
  responde leyendo. Los textos filosóficos no evalúan historia de la filosofía.
- Ninguna pregunta debe indagar por la opinión del evaluado.

## Cuándo la pregunta necesita imagen

Los **textos discontinuos** son el caso natural: caricatura, cómic, etiqueta,
infografía, aviso publicitario. Genera la imagen (ver `imagenes.md`) cuando el
estímulo sea una caricatura o un aviso; usa el bloque nativo `tabla` cuando el
texto discontinuo sea una tabla.
