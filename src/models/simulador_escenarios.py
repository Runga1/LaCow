import itertools
import pandas as pd

from src.models.simulador_ganado import EscenarioGanado, calcular_rentabilidad


def generar_escenarios():
    pesos_compra = [160, 180, 200]
    precios_compra_kg = [7500, 7800, 8200]
    pesos_venta = [380, 420, 450]
    precios_venta_kg = [8500, 9200, 9800]
    costos_pasto = [60000, 70000]
    costos_sal_med = [14000, 22000]
    meses_lista = [18, 24, 30]
    otros_costos_lista = [100000]

    resultados = []

    for combinacion in itertools.product(
        pesos_compra,
        precios_compra_kg,
        pesos_venta,
        precios_venta_kg,
        costos_pasto,
        costos_sal_med,
        meses_lista,
        otros_costos_lista,
    ):
        (
            peso_compra,
            precio_compra_kg,
            peso_venta,
            precio_venta_kg,
            costo_pasto,
            costo_sal_med,
            meses,
            otros_costos,
        ) = combinacion

        escenario = EscenarioGanado(
            peso_compra_kg=peso_compra,
            precio_compra_kg=precio_compra_kg,
            peso_venta_kg=peso_venta,
            precio_venta_kg=precio_venta_kg,
            costo_pasto_mensual=costo_pasto,
            costo_sal_med_mensual=costo_sal_med,
            meses=meses,
            otros_costos=otros_costos,
        )

        resultado = calcular_rentabilidad(escenario)

        fila = {
            "peso_compra_kg": peso_compra,
            "precio_compra_kg": precio_compra_kg,
            "peso_venta_kg": peso_venta,
            "precio_venta_kg": precio_venta_kg,
            "costo_pasto_mensual": costo_pasto,
            "costo_sal_med_mensual": costo_sal_med,
            "meses": meses,
            "otros_costos": otros_costos,
            **resultado,
        }

        resultados.append(fila)

    df = pd.DataFrame(resultados)
    return df


if __name__ == "__main__":
    df_escenarios = generar_escenarios()

    df_escenarios = df_escenarios.sort_values(
        by=["roi", "utilidad"], ascending=False
    )

    print(df_escenarios.head(10))

    df_escenarios.to_excel("outputs/escenarios_ganado.xlsx", index=False)
    print("Archivo guardado en outputs/escenarios_ganado.xlsx")