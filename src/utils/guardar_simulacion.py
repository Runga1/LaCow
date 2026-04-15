from pathlib import Path
import pandas as pd


def guardar_simulacion_excel(
    datos_entrada: dict,
    resultados: dict,
    ruta_salida: str = "outputs/historico_simulaciones.xlsx"
) -> None:
    """
    Guarda una simulación en un archivo Excel histórico.
    Si el archivo no existe, lo crea.
    Si ya existe, agrega una nueva fila.
    """

    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    fila = {**datos_entrada, **resultados}
    df_nuevo = pd.DataFrame([fila])

    if ruta.exists():
        df_existente = pd.read_excel(ruta)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_excel(ruta, index=False)