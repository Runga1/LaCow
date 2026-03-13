import pandas as pd

from src.models.simulador_ganado import EscenarioGanado, calcular_rentabilidad


def analizar_sensibilidad() -> pd.DataFrame:
    escenario_base = {
        "peso_compra_kg": 160,
        "precio_compra_kg": 7500,
        "peso_venta_kg": 450,
        "precio_venta_kg": 9200,
        "costo_pasto_mensual": 60000,
        "costo_sal_med_mensual": 15000,
        "meses": 12,
        "otros_costos": 100000,
    }

    variaciones_precio_venta = [-0.15, -0.10, -0.05, 0, 0.05]
    variaciones_pasto = [0, 0.10, 0.20]
    variaciones_peso_venta = [-30, -20, -10, 0, 10]

    resultados = []

    for var_pv in variaciones_precio_venta:
        for var_pasto in variaciones_pasto:
            for var_peso in variaciones_peso_venta:
                precio_venta_ajustado = escenario_base["precio_venta_kg"] * (1 + var_pv)
                costo_pasto_ajustado = escenario_base["costo_pasto_mensual"] * (1 + var_pasto)
                peso_venta_ajustado = escenario_base["peso_venta_kg"] + var_peso

                escenario = EscenarioGanado(
                    peso_compra_kg=escenario_base["peso_compra_kg"],
                    precio_compra_kg=escenario_base["precio_compra_kg"],
                    peso_venta_kg=peso_venta_ajustado,
                    precio_venta_kg=precio_venta_ajustado,
                    costo_pasto_mensual=costo_pasto_ajustado,
                    costo_sal_med_mensual=escenario_base["costo_sal_med_mensual"],
                    meses=escenario_base["meses"],
                    otros_costos=escenario_base["otros_costos"],
                )

                resultado = calcular_rentabilidad(escenario)

                resultados.append({
                    "var_precio_venta": var_pv,
                    "var_pasto": var_pasto,
                    "var_peso_venta": var_peso,
                    "precio_venta_kg_ajustado": precio_venta_ajustado,
                    "costo_pasto_mensual_ajustado": costo_pasto_ajustado,
                    "peso_venta_kg_ajustado": peso_venta_ajustado,
                    **resultado,
                })

    df = pd.DataFrame(resultados)
    return df


if __name__ == "__main__":
    df_sensibilidad = analizar_sensibilidad()

    df_sensibilidad = df_sensibilidad.sort_values(by=["roi", "utilidad"], ascending=False)

    print("\n--- TOP 10 ESCENARIOS DE SENSIBILIDAD ---")
    print(df_sensibilidad.head(10))

    df_sensibilidad.to_excel("outputs/sensibilidad_escenario_base.xlsx", index=False)
    print("\nArchivo guardado en: outputs/sensibilidad_escenario_base.xlsx")