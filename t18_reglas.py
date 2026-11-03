"""Hackaton IIA UADE - T18 | Clasificador simbolico de quiebre de stock.

Ejecutar desde la raiz del repositorio: python t18_reglas.py
Requiere Python 3.8+; utiliza solo bibliotecas estandar.
"""
from pathlib import Path
import csv

COBERTURA = "Días de cobertura (con el stock actual)"
VARIABILIDAD = "Variabilidad de la demanda (coeficiente de variación)"
DEMORA = "Demora del proveedor (días)"


def predecir(cobertura, variabilidad, demora):
    """Retorna 1 (SI) si demora > cobertura; de lo contrario 0 (NO).

    Variabilidad se recibe y valida para reflejar los datos disponibles,
    pero no participa en la regla inicial (limitacion documentada).
    """
    if any(not (0 <= x < float("inf")) for x in (cobertura, variabilidad, demora)):
        raise ValueError("Ingresar valores numericos finitos y no negativos.")
    return int(demora > cobertura)


def cargar_datos():
    rutas = [Path("datos/T18.csv"), Path("T18.csv"), Path(__file__).parent / "datos/T18.csv", Path(__file__).parent / "T18.csv"]
    ruta = next((p for p in rutas if p.is_file()), None)
    if ruta is None:
        raise FileNotFoundError("No se encontro datos/T18.csv ni T18.csv. Ejecutar desde la raiz del repositorio.")
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo))
    if len(filas) != 20:
        raise ValueError(f"Se esperaban 20 casos; se encontraron {len(filas)}.")
    casos = []
    for f in filas:
        casos.append({
            "caso": int(f["caso"]),
            "conjunto": f["conjunto"].strip().lower(),
            "cobertura": float(f[COBERTURA].replace(",", ".")),
            "variabilidad": float(f[VARIABILIDAD].replace(",", ".")),
            "demora": float(f[DEMORA].replace(",", ".")),
            "real": int(f["resultado_real"]),
        })
    if [f["caso"] for f in casos] != list(range(1, 21)):
        raise ValueError("Los casos deben estar numerados del 1 al 20 en orden.")
    if any(f["conjunto"] != ("entrenamiento" if f["caso"] <= 14 else "prueba") for f in casos):
        raise ValueError("Division no valida: casos 1-14 entrenamiento, 15-20 prueba.")
    return casos


def evaluar(casos, baseline=False):
    vp = vn = fp = fn = 0
    errores = []
    for f in casos:
        pred = 0 if baseline else predecir(f["cobertura"], f["variabilidad"], f["demora"])
        real = f["real"]
        if pred == 1 and real == 1:
            vp += 1
        elif pred == 0 and real == 0:
            vn += 1
        elif pred == 1 and real == 0:
            fp += 1
            errores.append((f["caso"], "FP"))
        else:
            fn += 1
            errores.append((f["caso"], "FN"))
    return vp, vn, fp, fn, errores


def porcentaje(numerador, denominador):
    return f"{100 * numerador / denominador:.2f}%" if denominador else "indefinida"


def informar(titulo, casos, baseline=False):
    vp, vn, fp, fn, errores = evaluar(casos, baseline=baseline)
    print(f"\n{titulo} ({len(casos)} casos)")
    print(f"                   Predice SI   Predice NO")
    print(f"Real SI                 {vp:2}            {fn:2}")
    print(f"Real NO                 {fp:2}            {vn:2}")
    print(f"Exactitud:     {porcentaje(vp + vn, len(casos))}")
    print(f"Precision:     {porcentaje(vp, vp + fp)}")
    print(f"Sensibilidad:  {porcentaje(vp, vp + fn)}")
    print(f"Especificidad: {porcentaje(vn, vn + fp)}")
    print(f"Errores: {errores if errores else 'ninguno'}")


def demo():
    print("\n=== DEMOSTRACION CON PRODUCTO NUEVO ===")
    print("Ingresar los datos conocidos ANTES de la semana que se predice.")
    try:
        cobertura = float(input("Dias de cobertura: ").replace(",", "."))
        variabilidad = float(input("Variabilidad de demanda (CV, p.ej. 0.3): ").replace(",", "."))
        demora = float(input("Demora del proveedor (dias): ").replace(",", "."))
        resultado = predecir(cobertura, variabilidad, demora)
    except (ValueError, EOFError) as error:
        print(f"No se pudo procesar el caso: {error}")
        return
    print(f"Prediccion: {'SI (1) - alerta de quiebre' if resultado else 'NO (0) - sin alerta'}")
    print(f"Regla: {demora:g} > {cobertura:g} es {'verdadero' if resultado else 'falso'}.")
    print("Limitacion: la variabilidad no altera la salida de esta version.")


def main():
    datos = cargar_datos()
    entrenamiento = [f for f in datos if f["conjunto"] == "entrenamiento"]
    prueba = [f for f in datos if f["conjunto"] == "prueba"]
    print("T18 - Reglas SI-ENTONCES | Quiebre de stock proxima semana")
    print("Regla fija: si demora_proveedor > dias_cobertura -> SI; sino -> NO")
    informar("SISTEMA - ENTRENAMIENTO", entrenamiento)
    informar("SISTEMA - PRUEBA", prueba)
    informar("LINEA BASE (siempre NO) - ENTRENAMIENTO", entrenamiento, baseline=True)
    informar("LINEA BASE (siempre NO) - PRUEBA", prueba, baseline=True)
    demo()


if __name__ == "__main__":
    main()
