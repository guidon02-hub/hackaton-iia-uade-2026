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
