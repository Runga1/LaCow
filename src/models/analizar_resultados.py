import pandas as pd


def analizar_resultados(path_resultados: str) -> None:
    df = pd.read_excel(path_resultados)

    if df.empty:
        print("El archivo de resultados está vacío.")
        return

    print("\n--- RESUMEN GENERAL ---")
    print(f"Número de escenarios: {len(df)}")
    print(f"ROI promedio: {df['roi'].mean():.2%}")
    print(f"Utilidad promedio: ${df['utilidad'].mean():,.0f}")
    print(f"Precio equilibrio promedio: ${df['precio_equilibrio_kg_venta'].mean():,.2f}")

    mejor_roi = df.loc[df["roi"].idxmax()]
    mayor_utilidad = df.loc[df["utilidad"].idxmax()]
    menor_equilibrio = df.loc[df["precio_equilibrio_kg_venta"].idxmin()]

    print("\n--- MEJOR ESCENARIO POR ROI ---")
    print(mejor_roi)

    print("\n--- ESCENARIO CON MAYOR UTILIDAD ---")
    print(mayor_utilidad)

    print("\n--- ESCENARIO CON MENOR PRECIO DE EQUILIBRIO ---")
    print(menor_equilibrio)

    escenarios_viables = df[
        (df["utilidad"] > 0) &
        (df["roi"] > 0.15)
    ]

    print("\n--- ESCENARIOS VIABLES (utilidad > 0 y ROI > 15%) ---")
    print(escenarios_viables[
        [
            "peso_compra_kg",
            "precio_compra_kg",
            "peso_venta_kg",
            "precio_venta_kg",
            "meses",
            "utilidad",
            "roi",
            "precio_equilibrio_kg_venta",
        ]
    ])

    escenarios_viables.to_excel("outputs/escenarios_viables.xlsx", index=False)
    print("\nArchivo guardado en: outputs/escenarios_viables.xlsx")

    # -----------------------------
    # TOP ESCENARIOS
    # -----------------------------

    print("\n--- TOP 5 POR ROI ---")
    top_roi = escenarios_viables.sort_values(by="roi", ascending=False).head(5)

    print(top_roi[
        [
            "peso_compra_kg",
            "precio_compra_kg",
            "peso_venta_kg",
            "precio_venta_kg",
            "utilidad",
            "roi",
            "costo_por_kg_ganado",
            "precio_equilibrio_kg_venta",
        ]
    ])

    print("\n--- TOP 5 POR UTILIDAD ---")
    top_utilidad = escenarios_viables.sort_values(by="utilidad", ascending=False).head(5)

    print(top_utilidad[
        [
            "peso_compra_kg",
            "precio_compra_kg",
            "peso_venta_kg",
            "precio_venta_kg",
            "utilidad",
            "roi",
            "costo_por_kg_ganado",
            "precio_equilibrio_kg_venta",
        ]
    ])

    top_roi.to_excel("outputs/top_roi.xlsx", index=False)
    top_utilidad.to_excel("outputs/top_utilidad.xlsx", index=False)

    print("\nArchivos guardados en:")
    print("outputs/top_roi.xlsx")
    print("outputs/top_utilidad.xlsx")


if __name__ == "__main__":
    analizar_resultados("outputs/escenarios_ganado_resultados.xlsx")