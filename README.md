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
