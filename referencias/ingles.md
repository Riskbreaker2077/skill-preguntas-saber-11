# Inglés — estructura oficial Saber 11.°

Fuente: `Base_MD/Guia_orientacion_Saber11_2026-2.md` (§E),
`Base_MD/Marco_referencia_ingles_saber11.md` y el cuadernillo real
`Base_MD/10_PRACTICA_INGLES.md`.

**Prueba real:** 55 preguntas en el cuadernillo (45 calificadas), 7 partes.

Esta prueba **no** se desagrega en competencias/afirmaciones/evidencias como
las otras cuatro: se organiza en **siete partes**, y a los evaluados se les
clasifica por nivel del **MCER**. Aun así, el formato exige los 6 campos de
metadata pedagógica, así que abajo se fija cómo llenarlos.

## Las siete partes

| Parte | % | Preguntas | Qué evalúa | Formato | Opciones |
|---|---|---|---|---|---|
| 1 | 11 % | 5 | Conocimiento lexical | 5 descripciones a emparejar con una lista de palabras A–G (+ H de ejemplo). Sobran dos. | A–G |
| 2 | 11 % | 5 | Conocimiento pragmático | Un aviso; el evaluado indica dónde puede verse. | A, B, C |
| 3 | 11 % | 5 | Conocimiento comunicativo | Completar conversaciones cortas con la intervención más adecuada. | A, B, C |
| 4 | 18 % | 8 | Conocimiento gramatical (uso del lenguaje) | Texto con espacios en blanco numerados; elegir la palabra de cada espacio. | A, B, C |
| 5 | 16 % | 7 | Comprensión de lectura literal | Texto + enunciados que parafrasean información explícita. | A, B, C |
| 6 | 11 % | 5 | Lectura inferencial | Texto + preguntas de inferencia, intención del autor, aspectos generales y particulares. | A, B, C, D |
| 7 | 22 % | 10 | Conocimiento gramatical y lexical | Texto con espacios numerados, nivel intermedio. | A, B, C, D |

> El *Marco de referencia* (documento más antiguo) numera las partes 1 y 2 al
> revés y menciona 8 opciones en el emparejamiento. Manda la Guía de
> orientación vigente y el cuadernillo real: **parte 1 = emparejamiento**,
> **parte 2 = avisos**, y el banco es A–G más H para el ejemplo.

## Cómo se representa cada parte en el formato

| Parte | Estructura del paquete |
|---|---|
| 1 | Grupo `banco_opciones`. El banco lleva las 7 palabras (A–G) más la del ejemplo con `"es_ejemplo": true`. Cada una de las 5 preguntas es `tipo_item: "miembro_banco_opciones"`, con su `enunciado` (la descripción), su `respuesta_pool_id` y su `justificacion`. |
| 2, 3 | Preguntas estándar independientes. En la parte 2 el aviso es una **imagen** en `contexto`; en la parte 3 el turno del interlocutor 1 va en `contexto` o `enunciado`. |
| 4, 7 | Grupo `texto_con_blancos`. El pasaje completo, con los blancos marcados inline como `(16)_______`, va una sola vez en `grupos[].contexto`. Cada pregunta es `tipo_item: "miembro_texto_con_blancos"`, sin `enunciado` propio, con `numero_blanco` y sus opciones. |
| 5, 6 | Grupo `contexto_compartido`: el artículo en `grupos[].contexto`, y cada pregunta con su `enunciado` y opciones propias. |

Detalles del formato en `formato-paquete.md`.

## Metadata pedagógica para Inglés

Rellena los 6 campos así (valores estables, no los inventes por pregunta):

```json
"competencia": "Competencia comunicativa en inglés",
"componente": "Parte 4 — Conocimiento gramatical (uso del lenguaje)",
"afirmacion": "Selecciona la palabra gramaticalmente adecuada para completar un texto de conocimiento general.",
"evidencia": "Completa un espacio de un texto eligiendo la forma gramatical correcta entre tres opciones.",
"estandar_asociado": "Comprendo textos escritos de mediana dificultad sobre temas de interés general.",
"que_evalua": "El uso del pretérito perfecto para señalar una acción con efecto en el presente."
```

Cuando el grupo comparte parte y nivel, pon los 6 campos una sola vez en
`grupos[].metadata_pedagogica` y no los repitas en cada miembro.

Añade siempre `nivel_mcer` (campo propio del estándar para lengua extranjera):

- **Pre A1** — no produce discurso; comprende palabras y expresiones fijas sueltas.
- **A1**, **A2** — nivel básico: partes 1 a 4 y la mitad de la 5.
- **B1** — nivel intermedio: partes 5 a 7.
- **B2** — techo de la prueba; solo para los ítems más exigentes de la parte 7.

La meta del MEN para la educación media es **B1**. No escribas ítems C1/C2.

`estandar_asociado` cita los Estándares Básicos de Competencias en Lenguas
Extranjeras: Inglés (MEN), grados 10.º–11.º, que están redactados por
habilidad. Ejemplos:

- «Comprendo textos escritos de mediana dificultad sobre temas de interés general.»
- «Identifico palabras clave dentro del texto que me permiten comprender su sentido general.»
- «Analizo textos descriptivos, narrativos y argumentativos con el fin de comprender las ideas principales.»
- «Comprendo variedad de textos informativos provenientes de diferentes fuentes.»

## Reglas de redacción propias del área

- Todo el contenido de la pregunta va **en inglés**: contexto, enunciado y
  opciones. Las **justificaciones van en español**, porque las lee el docente
  o el estudiante que revisa su resultado.
- Vocabulario y estructuras acordes al nivel MCER declarado. Un ítem A1 no
  puede exigir *present perfect continuous*.
- Los distractores deben ser errores plausibles reales (falsos amigos,
  concordancia, tiempo verbal equivocado), no palabras al azar.
- Temáticas de conocimiento general, sin carga cultural que exija haber
  vivido en un país específico.

## Cuándo la pregunta necesita imagen

La **parte 2 casi siempre la exige**: el aviso es una imagen (un letrero, una
etiqueta, una señal). Genérala con el tipo `aviso` de `imagenes.md`, y pon en
`descripcion_accesible` el texto del letrero.
