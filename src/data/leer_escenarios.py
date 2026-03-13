import pandas as pd


def leer_escenarios(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    columnas_esperadas = [
        "peso_compra_kg",
        "precio_compra_kg",
        "peso_venta_kg",
        "precio_venta_kg",
        "costo_pasto_mensual",
        "costo_sal_med_mensual",
        "meses",
        "otros_costos",
    ]

    faltantes = [col for col in columnas_esperadas if col not in df.columns]

    if faltantes:
        raise ValueError(f"Faltan columnas en el archivo: {faltantes}")

    return df