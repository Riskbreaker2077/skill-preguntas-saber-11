# Matemáticas — taxonomía oficial Saber 11.°

Fuente: `Base_MD/Guia_orientacion_Saber11_2026-2.md` (§A) y
`Base_MD/Marco_referencia_matematicas_saber11.md`.

**Prueba real:** 40 preguntas (25 en la primera sesión, 15 en la segunda).

Los textos de `competencia`, `afirmacion` y `evidencia` de abajo se copian
**literalmente** en el JSON. No los parafrasees: el valor del paquete está en
que un consumidor pueda agrupar preguntas por la misma cadena exacta.

**El número que encabeza cada afirmación y evidencia («1.», «2.3») es el
localizador de la tabla oficial, no parte del valor: no lo copies al JSON.**

## Competencias, afirmaciones y evidencias

| Competencia | Afirmación | Evidencias |
|---|---|---|
| Interpretación y representación (34 %) | 1. Comprende y transforma la información cuantitativa y esquemática presentada en distintos formatos. | 1.1 Da cuenta de las características básicas de la información presentada en diferentes formatos, como series, gráficas, tablas y esquemas.<br>1.2 Transforma la representación de una o más piezas de información. |
| Formulación y ejecución (43 %) | 2. Frente a un problema que involucre información cuantitativa, plantea e implementa estrategias que lleven a soluciones adecuadas. | 2.1 Diseña planes para la solución de problemas que involucran información cuantitativa o esquemática.<br>2.2 Ejecuta un plan de solución para un problema que involucra información cuantitativa o esquemática.<br>2.3 Resuelve un problema que involucra información cuantitativa o esquemática. |
| Argumentación (23 %) | 3. Valida procedimientos y estrategias matemáticas utilizadas para dar solución a problemas. | 3.1 Plantea afirmaciones que sustentan o refutan una interpretación dada a la información disponible en el marco de la solución de un problema.<br>3.2 Argumenta a favor o en contra de un procedimiento para resolver un problema a la luz de criterios presentados o establecidos.<br>3.3 Establece la validez o pertinencia de una solución propuesta a un problema dado. |

## Componentes (contenidos curriculares)

El campo `componente` toma uno de estos tres valores exactos:

- **Estadística**
- **Geometría**
- **Álgebra y cálculo**

### Contenidos por componente

| Componente | Genéricos | No genéricos |
|---|---|---|
| Estadística | Tipos de representación de datos (tablas y gráficas); intersección, unión y contenencia de conjuntos; promedio y rango; conteos simples con principios de suma y multiplicación; noción de población, muestra e inferencia muestral | Estimación del error; varianza, percentiles, mediana y correlación; combinaciones y permutaciones |
| Geometría | Triángulos, círculos, paralelogramos, esferas, paralelepípedos rectos, cilindros y sus medidas; paralelismo y ortogonalidad entre rectas; desigualdad triangular; sistemas de coordenadas cartesianas | Pirámides y polígonos de más de cuatro lados; congruencia y semejanza; teoremas de Pitágoras y de Tales; coordenadas polares y tridimensionales; transformaciones en el plano |
| Álgebra y cálculo | Racionales como fracciones, razones, decimales o porcentajes; propiedades de suma, resta, multiplicación, división y potenciación (incluida notación científica); relaciones lineales y afines y razones de cambio (tasas de interés, cambiarias, velocidad, aceleración) | Expresiones algebraicas y operaciones entre ellas; representación gráfica y algebraica de funciones racionales, trigonométricas, polinomiales, exponenciales y logarítmicas (periodicidad, dominios, rangos, crecimiento, intersecciones); sucesiones y sus límites |

**Regla del ICFES:** el uso de expresiones algebraicas es *siempre* no
genérico. Una pregunta genérica no debe exigir manipulación algebraica.

## Situaciones o contextos

Toda pregunta se sitúa en uno de estos cuatro escenarios:

- **Familiares o personales** — finanzas personales, hogar, transporte, salud, recreación.
- **Laborales u ocupacionales** — tareas de trabajo que no exigen conocimiento técnico de un oficio.
- **Comunitarios o sociales** — política, economía, convivencia, medioambiente.
- **Matemáticos o científicos** — situaciones abstractas, propias de las matemáticas; se asocian a contenidos no genéricos.

Los tres primeros son contextos cotidianos: úsalos para contenidos genéricos.

> El vocabulario de arriba es el **literal de Saber 11.°**. Si el encargo es
> alimentar un banco existente, copia primero el que ese banco ya use: ver
> «Integrarse a un banco existente» en `formato-banco.md`.

## Estándar asociado

`estandar_asociado` cita un Estándar Básico de Competencias en Matemáticas
(MEN) del ciclo 10.º–11.º, en primera persona. Ejemplos válidos:

- «Interpreto y comparo resultados de estudios con información estadística provenientes de medios de comunicación.»
- «Modelo situaciones de variación periódica con funciones trigonométricas.»
- «Diseño estrategias para abordar situaciones de medición que requieran grados de precisión específicos.»
- «Justifico o refuto inferencias basadas en razonamientos estadísticos a partir de resultados de estudios publicados.»
- «Uso argumentos geométricos para resolver y formular problemas en contextos matemáticos y en otras ciencias.»

## Cuándo la pregunta necesita imagen

Muy frecuente en esta prueba. Genera imagen (ver `imagenes.md`) cuando el
estímulo sea una gráfica de barras, líneas, dispersión o torta; un plano
cartesiano con una o más funciones; o una figura geométrica acotada.
Cuando el estímulo sea **una tabla de datos**, usa el bloque nativo
`{"tipo":"tabla"}` en vez de una imagen: es texto, se lee con lector de
pantalla y no se pixela.
