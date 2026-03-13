import pandas as pd

from src.data.leer_escenarios import leer_escenarios
from src.models.simulador_ganado import EscenarioGanado, calcular_rentabilidad


def procesar_escenarios(path_entrada: str, path_salida: str) -> pd.DataFrame:
    df = leer_escenarios(path_entrada)

    resultados = []

    for _, fila in df.iterrows():
        escenario = EscenarioGanado(
            peso_compra_kg=float(fila["peso_compra_kg"]),
            precio_compra_kg=float(fila["precio_compra_kg"]),
            peso_venta_kg=float(fila["peso_venta_kg"]),
            precio_venta_kg=float(fila["precio_venta_kg"]),
            costo_pasto_mensual=float(fila["costo_pasto_mensual"]),
            costo_sal_med_mensual=float(fila["costo_sal_med_mensual"]),
            meses=int(fila["meses"]),
            otros_costos=float(fila["otros_costos"]),
        )

        resultado = calcular_rentabilidad(escenario)

        resultados.append({
            **fila.to_dict(),
            **resultado
        })

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel(path_salida, index=False)

    return df_resultados


if __name__ == "__main__":
    entrada = "data/raw/escenarios_ganado.xlsx"
    salida = "outputs/escenarios_ganado_resultados.xlsx"

    df_resultados = procesar_escenarios(entrada, salida)
    print(df_resultados.head())
    print(f"\nArchivo guardado en: {salida}")