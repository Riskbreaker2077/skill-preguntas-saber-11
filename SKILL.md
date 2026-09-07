---
name: preguntas-saber-11
description: Genera preguntas tipo ICFES Saber 11.° de Matemáticas, Lectura Crítica, Sociales y Ciudadanas, Ciencias Naturales o Inglés, con la metadata pedagógica oficial (competencia, componente, afirmación, evidencia, estándar asociado), justificación por cada opción y, cuando el ítem lo exige, la imagen del estímulo generada como PNG. Entrega un ZIP en el formato abierto preguntas-icfes, ya validado. Úsala cuando pidan preguntas ICFES, preguntas tipo Saber 11, un simulacro, un banco de preguntas, un cuestionario de una prueba del ICFES o preguntas con gráfica o imagen para alguna de esas cinco áreas. Palabras que la disparan - ICFES, Saber 11, pregunta tipo ICFES, simulacro, banco de preguntas, competencia, afirmación, evidencia, cuadernillo, prueba de Estado.
---

# Preguntas tipo ICFES Saber 11.°

Produce un **ZIP con un archivo JSON por pregunta**, en el formato abierto
[`preguntas-icfes`](https://github.com/Riskbreaker2077/preguntas-icfes) y con
la organización del banco
[`banco-preguntas-icfes`](https://github.com/Riskbreaker2077/banco-preguntas-icfes),
de modo que se descomprima encima de un banco existente sin colisiones. Todo
se apoya en la documentación oficial del ICFES convertida a Markdown en
`Base_MD/`.

## Qué preguntar antes de empezar

Solo lo que no puedas inferir del encargo. Con una sola ronda basta:

1. **Área** — Matemáticas, Lectura Crítica, Sociales y Ciudadanas, Ciencias Naturales o Inglés.
2. **Cuántas preguntas.**
3. **Enfoque** — ¿una competencia, componente o tema concreto, o distribución realista según los porcentajes oficiales del área?
4. **Imágenes** — ¿alguna pregunta debe llevar estímulo gráfico? Si el encargo no lo dice, propón el número que salga natural del área y sigue.
5. **Destino** — ¿es una entrega autónoma, o va a sumarse a un banco existente? Si va a un banco, necesitas su ruta: de ahí salen los ids libres y el vocabulario que hay que copiar.

Si el encargo ya trae todo eso, no preguntes: ponte a escribir.

## El flujo

### 1. Lee la referencia del área

| Área | Archivo |
|---|---|
| Matemáticas | `referencias/matematicas.md` |
| Lectura Crítica | `referencias/lectura-critica.md` |
| Sociales y Ciudadanas | `referencias/sociales-ciudadanas.md` |
| Ciencias Naturales | `referencias/ciencias-naturales.md` |
| Inglés | `referencias/ingles.md` |

Trae la tabla de competencias, afirmaciones y evidencias, los valores válidos
de `componente`, los porcentajes oficiales y ejemplos de `estandar_asociado`.

Lee **siempre** `referencias/construccion-items.md`: son las reglas del ICFES
para redactar ítems y la lista de verificación final. No es opcional.

Si necesitas más contexto del que trae la referencia —el tono real de los
ítems, un tema poco cubierto—, ve a `Base_MD/`: los `Marco_referencia_*.md`
explican qué se evalúa, los `*_PRACTICA_*.md` traen preguntas reales de
aplicaciones anteriores y los `*_EXPLICADAS_*.md` muestran cómo el ICFES
justifica cada opción. **Léelos para calibrar, nunca para copiar un ítem.**

### 2. Planea el paquete antes de escribirlo

Para cada pregunta, decide primero: **evidencia → tarea de evaluación →
estímulo → dificultad → si lleva imagen**. Es el orden del Diseño Centrado en
Evidencias, y evita el error clásico de escribir una pregunta bonita que no
mide la evidencia que dice medir.

Reparte competencias y componentes según los porcentajes oficiales del área
cuando el encargo pida un conjunto representativo. Equilibra la posición de la
clave entre A, B, C y D.

Decide qué preguntas comparten estímulo: un texto de Lectura Crítica que
sostiene cuatro preguntas es **un grupo**, no cuatro copias del texto. Ver
«Grupos» en `referencias/formato-banco.md`.

### 3. Monta la carpeta de trabajo

```
salida/<nombre>/
├── _specs/                        ← especificaciones de las imágenes (fuera del ZIP)
└── banco/
    └── <area-slug>/
        ├── <id>.json              ← una pregunta por archivo, el nombre es su id
        ├── grupos/<id>.json
        ├── imagenes/<id>-N.png
        └── fuentes/               ← solo si transcribes de un PDF oficial
```

Los slugs de área y los prefijos de id (`ciencias-sociales`/`cs`,
`lenguaje`/`lg`, `matematicas`/`mt`, `ciencias-naturales`/`cn`, `ingles`/`in`)
están en `referencias/formato-banco.md`. Reserva los ids de una vez:

```bash
python3 scripts/siguiente_id.py <carpeta-del-area> --cuantos 20
python3 scripts/siguiente_id.py <carpeta-del-area> --grupo
```

Si la entrega va a sumarse a un banco existente, apúntalo a **ese** banco para
que la numeración continúe la suya. Parte de `plantillas/pregunta.json` y
`plantillas/grupo.json`. El contrato completo está en
`referencias/formato-banco.md`.

### 4. Genera las imágenes

Solo las que hagan falta. `referencias/imagenes.md` tiene los siete tipos
disponibles (barras, líneas, dispersión, torta, cartesiano, esquema, aviso),
cuándo usar un bloque `tabla` en vez de una imagen, y cómo escribir la
`descripcion_accesible`.

```bash
python3 scripts/imagen.py --lote salida/<nombre>/_specs \
    salida/<nombre>/banco/<area>/imagenes
```

Cada imagen se llama `<id>-N.png` con el id de la pregunta o del grupo que la
usa. Nombra las especificaciones igual, para que `--lote` produzca el nombre
correcto sin renombrar nada.

Mira los PNG que generaste antes de seguir. Una gráfica con etiquetas
encimadas o una escala mal elegida invalida la pregunta.

### 5. Valida y empaqueta

```bash
python3 scripts/empaquetar.py salida/<nombre>
```

Envuelve cada área en un paquete sintético y la pasa por el validador de
referencia del propio estándar. Los errores (`✗`) bloquean el ZIP; los avisos
(`⚠`) señalan problemas de calidad —clave desbalanceada, imagen sin
descripción accesible, `version_estandar` sin declarar— que debes resolver,
no ignorar.

### 6. Entrega

Da la ruta del `.zip` y un resumen breve: cuántas preguntas, qué rango de ids
ocupan, cómo quedaron repartidas por competencia y componente, cuáles llevan
imagen, y **qué quedó pendiente de revisión humana**. Si va a un banco, di
que se descomprime desde su raíz.

## Reglas innegociables

**Procedencia honesta.** Todo lo que generes va con
`procedencia: {contenido, clasificacion, respuesta_correcta}` en
`"ia_generada"` y `verificado` en `false` en los tres bloques. Solo se marca
`"oficial"` o `"extraido_oficial"` lo transcrito de un documento del ICFES, y
entonces el PDF va en `fuentes/` y se nombra en el campo `fuentes`.
`verificado: true` lo pone la persona que revisó, jamás la skill.

**Ítems originales.** El manual del ICFES lo exige. Los cuadernillos de
`Base_MD/` son para calibrar el estilo y la dificultad, no para reciclar
preguntas. Si el encargo pide transcribir ítems oficiales, eso es otra tarea:
transcríbelos marcando la procedencia real y guarda el PDF en `fuentes/`.

**Metadata literal.** `competencia`, `componente`, `afirmacion` y `evidencia`
se copian palabra por palabra. Parafrasearlas rompe el valor del paquete: un
consumidor agrupa por cadena exacta. **De dónde se copian depende del
destino**: de la referencia del área si la entrega es autónoma, o del
vocabulario que el banco ya use si va a sumarse a uno. Los dos existen y no
son intercambiables — mira qué hay en el destino antes de escribir, y si no
está claro, pregunta. Ver «Integrarse a un banco existente» en
`referencias/formato-banco.md`.

**`version_estandar` en cada pregunta.** Fuera de un paquete envolvente, el
archivo suelto no tiene otra forma de autodescribirse. Es la versión mínima
que exigen los campos que usa, no la de hoy: `scripts/banco.py` la calcula con
`version_minima()`.

**Una justificación por opción, y específica.** La de la clave explica el
razonamiento; la de cada distractor nombra el error concreto que comete quien
lo elige. «No es la respuesta correcta» no es una justificación.

**Cuatro opciones**, salvo las partes 2 a 5 de Inglés, que usan tres por
diseño oficial.

**Sin nombres propios** de personas, empresas, municipios o departamentos.
**Sin opiniones**: ninguna pregunta indaga por lo que piensa el evaluado, ni
tiene una clave que dependa del criterio de quien la escribió.

**Revisa antes de empaquetar.** La lista de verificación al final de
`referencias/construccion-items.md`, ítem por ítem. Es lo que separa un
paquete usable de uno que un docente tiene que rehacer.

## Mapa del repo

| Ruta | Qué es |
|---|---|
| `referencias/` | Taxonomías por área, reglas de construcción, contrato del formato, guía de imágenes |
| `scripts/imagen.py` | Genera PNG desde una especificación JSON |
| `scripts/empaquetar.py` | Valida y arma el ZIP |
| `scripts/vendor/validar.js` | Validador de referencia del estándar (copia verbatim) |
| `scripts/banco.py` | Lee un banco en disco y lo envuelve para validarlo |
| `scripts/siguiente_id.py` | Próximo id libre de un área |
| `plantillas/` | Esqueleto de una pregunta y de un grupo |
| `ejemplos/` | Un banco completo y válido, con imagen y grupo |
| `Base_MD/` | Los 20 documentos oficiales del ICFES en Markdown |
| `Base/` | Los PDF originales (no versionados; ver `Base_MD/MANIFEST.md`) |
