T18 · Predicción de quiebre de stock en la cadena de suministro

Hackatón IIA · UADE · 3.4.257 · 3 de noviembre de 2026

Integrantes: Guido Guzzetti · Ruan Bezerra

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

**Cómo decide.**

Desarrollamos un sistema de inteligencia artificial simbólica basado en reglas SI-ENTONCES para anticipar posibles quiebres de stock.

El sistema aplica las siguientes reglas:

- R1: SI la demora del proveedor es mayor que los días de cobertura del inventario, ENTONCES clasificar SÍ (riesgo de quiebre de stock).
- R2: SI la demora del proveedor es menor o igual que los días de cobertura, ENTONCES clasificar NO (sin alerta de quiebre).

La lógica consiste en comparar el tiempo durante el cual el inventario alcanza para cubrir la demanda con el tiempo necesario para recibir nueva mercadería.

Esta comparación funciona como una heurística de riesgo de abastecimiento, no como una garantía de que ocurrirá un quiebre durante la semana siguiente.

**Variables que usa y por qué.**

1. Días de cobertura: indica cuánto tiempo puede sostenerse la demanda con el inventario disponible. Es relevante porque una cobertura reducida aumenta el riesgo de faltantes.
2. Demora del proveedor: representa los días necesarios para recibir una reposición. Si supera la cobertura, existe riesgo de agotar el inventario antes de recibir mercadería.
3. Variabilidad de la demanda: representa cuánto fluctúa la demanda respecto de su promedio. Es relevante, pero la versión inicial del sistema no la incorpora directamente a la regla. Esto constituye una limitación del modelo.

La variable `resultado_real` no se utiliza para decidir, ya que representa lo que efectivamente ocurrió y solamente se conoce después. Se utiliza para evaluar las predicciones.

**Cómo se corre en vivo.**

El sistema está implementado en Python y puede ejecutarse en Google Colab o cualquier entorno compatible.

Código:

```python
def evaluar_stock(cobertura, variabilidad, demora):
    if cobertura < 0 or variabilidad < 0 or demora < 0:
        raise ValueError("Los valores no pueden ser negativos")

    if demora > cobertura:
        return "SÍ"
    else:
        return "NO"


# Ingreso de un caso nuevo
cobertura = float(input("Días de cobertura: "))
variabilidad = float(input("Variabilidad de demanda: "))
demora = float(input("Demora del proveedor (días): "))

resultado = evaluar_stock(cobertura, variabilidad, demora)

print("Predicción de quiebre de stock:", resultado)
```

El código recibe los valores de un producto nuevo y genera una clasificación de manera automática. No necesita conocer el resultado real del caso.

**Dos casos de ejemplo.**

| Caso inventado | Valores | Salida del sistema |
|---|---|---|
| A | Cobertura = 5 días; variabilidad = 0,30; demora = 8 días | SÍ |
| B | Cobertura = 12 días; variabilidad = 0,30; demora = 5 días | NO |

**Justificación de los ejemplos.**

Caso A: la demora supera la cobertura por 3 días. El sistema genera una alerta porque podría agotarse el inventario antes de recibir una reposición.

Caso B: la cobertura supera la demora por 7 días. El sistema no genera una alerta según la regla establecida.

**Limitaciones.**

La regla no utiliza directamente la variabilidad de la demanda ni modela la cantidad concreta que se espera vender durante los próximos siete días. Además, presupone que la cobertura y la demora representan adecuadamente las condiciones de abastecimiento.

Por lo tanto, es un sistema inicial, interpretable y reproducible, cuya utilidad debe evaluarse comparando sus predicciones con los resultados reales del dataset.

## 3. Medición

Para evaluar nuestro sistema utilizamos los 20 casos proporcionados en `datos/T18.csv`, respetando la separación obligatoria establecida por la cátedra:

- Entrenamiento: casos 1 a 14.
- Prueba: casos 15 a 20.

La clase positiva es SÍ (1): el producto se queda sin stock la semana siguiente.

La predicción se realiza con la regla definida en la sección 2: si la demora del proveedor supera los días de cobertura, el sistema predice SÍ. En caso contrario, predice NO.

### Entrenamiento (casos 1–14)

| | Predice SÍ | Predice NO |
|---|---:|---:|
| **Real SÍ** | VP = 5 | FN = 0 |
| **Real NO** | FP = 2 | VN = 7 |

**Verificación:** 5 + 0 + 2 + 7 = 14 casos.

- Verdaderos positivos (5): casos 3, 4, 5, 7 y 11.
- Falsos positivos (2): casos 2 y 10.
- Falsos negativos (0): ninguno.
- Verdaderos negativos (7): casos 1, 6, 8, 9, 12, 13 y 14.

### Prueba (casos 15–20)

| | Predice SÍ | Predice NO |
|---|---:|---:|
| **Real SÍ** | VP = 4 | FN = 0 |
| **Real NO** | FP = 1 | VN = 1 |

**Verificación:** 4 + 0 + 1 + 1 = 6 casos.

- Verdaderos positivos (4): casos 15, 16, 17 y 20.
- Falsos positivos (1): caso 18.
- Falsos negativos (0): ninguno.
- Verdaderos negativos (1): caso 19.

### Métricas de evaluación

| Métrica | Entrenamiento | Prueba |
|---|---:|---:|
| Exactitud | 85,71 % | 83,33 % |
| Precisión | 71,43 % | 80,00 % |
| Sensibilidad | 100,00 % | 100,00 % |
| Especificidad | 77,78 % | 50,00 % |

**Cálculo de las métricas**

**Exactitud = (VP + VN) / Total**

- Entrenamiento: (5 + 7) / 14 = 85,71 %.
- Prueba: (4 + 1) / 6 = 83,33 %.

**Precisión = VP / (VP + FP)**

- Entrenamiento: 5 / (5 + 2) = 71,43 %.
- Prueba: 4 / (4 + 1) = 80,00 %.

**Sensibilidad = VP / (VP + FN)**

- Entrenamiento: 5 / (5 + 0) = 100 %.
- Prueba: 4 / (4 + 0) = 100 %.

**Especificidad = VN / (VN + FP)**

- Entrenamiento: 7 / (7 + 2) = 77,78 %.
- Prueba: 1 / (1 + 1) = 50 %.

### Entrenamiento contra prueba

La exactitud disminuye de 85,71 % en entrenamiento a 83,33 % en prueba, una diferencia de 2,38 puntos porcentuales.

La sensibilidad se mantiene en 100 % en ambos conjuntos, lo que significa que nuestro sistema detectó todos los casos de quiebre de stock presentes en los datos.

Sin embargo, la especificidad disminuye de 77,78 % a 50 %. Esto significa que el sistema identifica correctamente una proporción menor de los casos sin quiebre en el conjunto de prueba.

La precisión aumenta de 71,43 % a 80 %, aunque este cambio debe interpretarse con precaución por el tamaño reducido de la muestra.

**Sobreajuste y generalización**

No observamos una caída importante de exactitud entre los dos conjuntos, pero esto no demuestra que el sistema generalice correctamente ante cualquier situación real.

El conjunto de prueba contiene solamente seis productos, por lo que las métricas pueden variar mucho ante nuevos casos.

Además, nuestro sistema es deliberadamente simple: utiliza una regla explícita y no fue construido para memorizar las etiquetas individuales del conjunto de entrenamiento.

Por lo tanto, podemos afirmar que el desempeño observado es similar en exactitud entre entrenamiento y prueba, pero no que esté demostrada su capacidad de generalización a una operación logística real.

### Conclusión de la medición

El sistema consigue detectar los nueve quiebres de stock reales incluidos en los 20 casos, sin falsos negativos, pero produce tres falsas alarmas.

Este resultado favorece el objetivo de anticipar quiebres de stock, aunque implica costos potenciales por reposiciones urgentes innecesarias.

La evaluación demuestra la importancia de utilizar varias métricas y no depender exclusivamente de la exactitud.

## 4. El error más caro

En nuestro problema de abastecimiento identificamos dos tipos de errores que producen consecuencias distintas.

**Falso positivo (FP):** el sistema predice que un producto se quedará sin stock, pero en realidad no ocurre. Según la ficha T18, esto puede provocar una reposición urgente innecesaria, generando costos adicionales de transporte y sobrestock.

**Falso negativo (FN):** el sistema predice que un producto no se quedará sin stock, pero efectivamente ocurre un quiebre. Esto puede provocar ventas perdidas y que un cliente elija comprar a la competencia.

**¿Cuál es el error más caro?**

Consideramos más costoso el falso negativo porque el centro de distribución no anticipa la falta de mercadería y pierde la oportunidad de intervenir preventivamente.

Además de perder ventas durante el período sin stock, existe el riesgo de deteriorar la relación comercial con los clientes.

Aunque un falso positivo también genera costos, priorizamos detectar los quiebres reales antes que reducir al máximo la cantidad de alertas.

**¿Qué cambiamos en el sistema para reducir ese error?**

Como decisión de diseño, elegimos una regla de alerta preventiva:

SI demora_proveedor > dias_cobertura, ENTONCES predecir SÍ.

En lugar de utilizar una estrategia conservadora que solamente emita alertas ante condiciones extremas, esta regla activa la alerta cuando el tiempo de reposición supera la cobertura del inventario.

Esta decisión busca reducir los falsos negativos, aunque puede aumentar los falsos positivos.

**Resultados observados:**

| Resultado | Entrenamiento | Prueba |
|---|---:|---:|
| Falsos negativos | 0 | 0 |
| Falsos positivos | 2 | 1 |
| Sensibilidad | 100 % | 100 % |

La regla detectó todos los quiebres reales incluidos en los 20 casos disponibles, a costa de tres falsas alarmas.

**Limitación:** el sistema no garantiza ausencia de falsos negativos en casos futuros. Los resultados corresponden únicamente al dataset del hackatón.

**Conclusión:** preferimos tolerar algunas alertas innecesarias para disminuir el riesgo de no detectar productos que pueden quedarse sin stock. Esta elección responde a las consecuencias comerciales establecidas en nuestra ficha y no solamente a maximizar la exactitud.

## 5. ¿Comparado contra qué?

**Línea base trivial.**

Para determinar si nuestro sistema realmente aporta valor, lo comparamos contra un clasificador trivial que siempre responde la clase mayoritaria del conjunto de entrenamiento.

De los 14 casos de entrenamiento, 9 corresponden a productos que no se quedaron sin stock (NO) y 5 a productos que sí se quedaron sin stock (SÍ).

Por lo tanto, la línea base predice siempre NO, independientemente de los días de cobertura, la variabilidad de la demanda o la demora del proveedor.

**Resultados de la comparación**

| Indicador | Línea base trivial | Nuestro sistema |
|---|---:|---:|
| Exactitud entrenamiento | 64,29 % | 85,71 % |
| Exactitud prueba | 33,33 % | 83,33 % |
| Sensibilidad entrenamiento | 0 % | 100 % |
| Sensibilidad prueba | 0 % | 100 % |
| Especificidad entrenamiento | 100 % | 77,78 % |
| Especificidad prueba | 100 % | 50 % |

La línea base acierta 9 de 14 casos de entrenamiento y 2 de 6 casos de prueba.

Nuestro sistema acierta 12 de 14 casos de entrenamiento y 5 de 6 casos de prueba.

La exactitud aumenta 21,42 puntos porcentuales en entrenamiento y 50 puntos porcentuales en prueba.

Sin embargo, la diferencia más importante para nuestro objetivo está en la sensibilidad.

La línea base nunca detecta un quiebre de stock porque siempre responde NO. Por eso tiene sensibilidad del 0 %.

Nuestro sistema alcanza una sensibilidad del 100 % en ambos conjuntos, detectando todos los quiebres reales de los datos disponibles.

Como contrapartida, la línea base presenta una especificidad del 100 %, mientras que nuestro modelo produce algunas falsas alarmas. Esto refleja el costo de priorizar la detección de quiebres.

La precisión de la línea base queda indefinida, porque nunca predice la clase positiva y el denominador VP + FP es cero.

**Conclusión de la comparación.**

Nuestro modelo supera a la línea base en exactitud y sensibilidad, aunque presenta menor especificidad.

Dado que en nuestra problemática un quiebre no detectado puede ocasionar ventas perdidas y pérdida de clientes, consideramos más útil el comportamiento de nuestro sistema que el de una estrategia que nunca emite alertas.

Esta conclusión se limita a los datos ficticios disponibles y no demuestra por sí sola el desempeño en un centro de distribución real.

### Checklist crítico de la Clase 6

| Checklist | Respuesta |
|---|---|
| ¿Qué datos? | Los 20 casos ficticios del grupo T18, proporcionados por la cátedra. Se utilizaron 14 casos de entrenamiento y 6 de prueba, sin modificar la división original. |
| ¿Qué métrica? | Sensibilidad como medida principal, complementada con exactitud, precisión y especificidad. |
| ¿Comparado contra qué? | Un clasificador trivial que siempre predice NO, por ser la clase mayoritaria del entrenamiento. |
| ¿Quién lo midió? | El grupo T18, con asistencia de ChatGPT para calcular las matrices y métricas a partir de los datos de la cátedra. Los resultados son reproducibles mediante las reglas publicadas. |

**Evaluación crítica.**

La exactitud por sí sola podría llevar a conclusiones equivocadas, porque no distingue entre detectar un quiebre real y acertar que un producto no sufrirá un faltante.

Por eso evaluamos especialmente la sensibilidad y la cantidad de falsos negativos, sin omitir los falsos positivos.

Los resultados permiten describir el comportamiento del sistema en los 20 casos ficticios, pero no garantizan su efectividad en una operación logística real.

Para validar un uso real sería necesario contar con más observaciones, medir costos económicos y evaluar el sistema sobre nuevos períodos de abastecimiento.

## 6. Riesgo: el camino completo

Nuestro sistema utiliza información sobre inventarios y tiempos de reposición para anticipar posibles quiebres de stock.

Un riesgo importante es que los datos de entrada estén desactualizados o sean incorrectos.

**Cadena de riesgo: datos → modelo → decisión → consecuencia**

**1. Datos:** el sistema recibe que un producto tiene 12 días de cobertura, cuando en realidad, por diferencias de inventario o registros desactualizados, solamente tiene 4 días. La demora del proveedor es de 8 días.

**2. Modelo:** al comparar los valores recibidos, la regla evalúa si 8 > 12. Como esta condición es falsa, predice NO. Sin embargo, con los datos correctos, 8 > 4 y la regla habría emitido una alerta.

**3. Decisión:** el planificador recibe una clasificación sin alerta y podría no priorizar la revisión o reposición urgente del producto.

**4. Consecuencia:** el inventario podría agotarse antes de recibir mercadería, ocasionando ventas perdidas y posibles pérdidas de clientes.

**¿Por qué es importante?**

Aunque el algoritmo aplique correctamente sus reglas, una entrada equivocada puede generar una decisión perjudicial.

Por lo tanto, una predicción técnicamente coherente con los datos ingresados no necesariamente representa la situación real del inventario.

**Medidas para reducir el riesgo:**

- Actualizar periódicamente los registros de inventario.
- Verificar los tiempos de entrega de los proveedores.
- Validar que los valores ingresados sean coherentes y no negativos.
- Mantener la supervisión humana sobre las decisiones de reposición.
- Revisar los casos en los que el sistema no emite una alerta, especialmente cuando la cobertura es reducida.

**Conclusión.**

La calidad del sistema no depende únicamente de la regla de clasificación, sino también de la confiabilidad de los datos y de cómo se utilizan sus predicciones para tomar decisiones.

Por eso proponemos utilizarlo como herramienta de apoyo al planificador y no como un mecanismo que ejecute automáticamente compras urgentes sin supervisión.

## 7. Bitácora

**Uso de la IA**

| # | Qué le pedimos | Qué aceptamos | Qué rechazamos y por qué |
|---|---|---|---|
| 1 | <> | <> | <> |

**Corridas contra el evaluador**

| Corrida | Nota | Agujero que encontró | Qué cambiamos |
|---|---|---|---|
| 1 | <> | <> | <> |
