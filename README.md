T18 · Predicción de quiebre de stock en la cadena de suministro

Hackatón IIA · UADE · 3.4.257 · 3 de noviembre de 2026

Integrantes: Guido Guzzetti · [Segundo integrante]

IA declarada: ChatGPT

Pista: Reglas

Publicación en LinkedIn: Pendiente

---

## 1. Formulación y PEAS

**La pregunta.** Para cada producto (SKU) del centro de distribución, ¿se quedará sin stock durante la próxima semana?

**SÍ (1):** el producto se queda sin stock la semana siguiente.

**NO (0):** el producto no se queda sin stock la semana siguiente.

El planificador de abastecimiento utiliza el sistema para identificar anticipadamente productos en riesgo y decidir cuáles requieren una revisión para reposición urgente.

| PEAS | Nuestro sistema |
|---|---|
| Medida de rendimiento | Detectar correctamente los quiebres de stock mediante la sensibilidad, controlando falsas alertas con la precisión y especificidad. También se calcula la exactitud. |
| Entorno | Centro de distribución con productos (SKU), inventarios, demanda variable y proveedores con diferentes tiempos de reposición. |
| Actuadores | Emitir alertas de riesgo de quiebre de stock o informar que no se detecta riesgo, para apoyar las decisiones del planificador. |
| Sensores | Días de cobertura del inventario actual, variabilidad de la demanda (coeficiente de variación) y demora del proveedor en días. |

**Objetivo y métrica.**

El objetivo operativo es reducir los quiebres de stock que ocasionan ventas perdidas y posible pérdida de clientes, evitando al mismo tiempo los costos de reposiciones urgentes innecesarias.

Para evaluar el sistema utilizamos como métrica principal la **sensibilidad**:

Sensibilidad = VP / (VP + FN)

Esta métrica indica qué proporción de los quiebres de stock reales fueron detectados por el sistema.

Elegimos priorizarla porque un falso negativo significa no anticipar un quiebre de stock, lo cual puede ocasionar ventas perdidas y la pérdida de clientes.

Sin embargo, una sensibilidad elevada no garantiza por sí sola una buena decisión de abastecimiento. Demasiadas alertas incorrectas pueden generar fletes urgentes y sobrestock.

Por eso también evaluamos la precisión, la especificidad y la exactitud, y posteriormente comparamos los resultados contra una línea base trivial.

**El objetivo y la métrica no son lo mismo:** el objetivo es mejorar el abastecimiento y reducir sus consecuencias negativas; la métrica cuantifica el desempeño del sistema para detectar casos positivos.

## 2. El sistema

**Cómo decide.** <Neurona: pesos y sesgo. Reglas: la lista de reglas si‑entonces. Agente: la regla con la que elige la acción.>

**Variables que usa y por qué.** <Cuáles usa, cuáles descarta y por qué.>

**Cómo se corre en vivo.** <Pasos concretos para resolver un caso nuevo: link al Colab, a la planilla o la cuenta a mano.>

**Dos casos de ejemplo.**

| Caso inventado | Valores | Salida del sistema |
|---|---|---|
| A | <…> | <SÍ/NO> |
| B | <…> | <SÍ/NO> |

## 3. Medición

**Entrenamiento (casos 1–14)**

| | Predice SÍ | Predice NO |
|---|---|---|
| **Real SÍ** | VP = <> | FN = <> |
| **Real NO** | FP = <> | VN = <> |

**Prueba (casos 15–20)**

| | Predice SÍ | Predice NO |
|---|---|---|
| **Real SÍ** | VP = <> | FN = <> |
| **Real NO** | FP = <> | VN = <> |

| Métrica | Entrenamiento | Prueba |
|---|---|---|
| Exactitud | <> | <> |
| Precisión | <> | <> |
| Sensibilidad | <> | <> |
| Especificidad | <> | <> |

**Entrenamiento contra prueba.** <¿Hay diferencia? ¿Por qué? ¿Sobreajuste o generalización?>

## 4. El error más caro

<¿Es peor el falso positivo o el falso negativo en su problema? ¿Por qué, según la ficha? ¿Qué cambiaron en el sistema para cometer menos ese error?>

## 5. ¿Comparado contra qué?

**Línea base trivial.** <Qué resultado saca un sistema que responde siempre lo mismo, y cómo se compara el suyo.>

| Checklist (Clase 6) | Respuesta |
|---|---|
| ¿Qué datos? | <> |
| ¿Qué métrica? | <> |
| ¿Comparado contra qué? | <> |
| ¿Quién lo midió? | <> |

## 6. Riesgo: el camino completo

<Datos → modelo → decisión → consecuencia aplicado a su caso. Al menos un riesgo concreto.>

## 7. Bitácora

**Uso de la IA**

| # | Qué le pedimos | Qué aceptamos | Qué rechazamos y por qué |
|---|---|---|---|
| 1 | <> | <> | <> |

**Corridas contra el evaluador**

| Corrida | Nota | Agujero que encontró | Qué cambiamos |
|---|---|---|---|
| 1 | <> | <> | <> |
