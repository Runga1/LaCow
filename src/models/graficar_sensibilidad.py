import pandas as pd
import matplotlib.pyplot as plt


def graficar_sensibilidad(path_archivo: str) -> None:
    df = pd.read_excel(path_archivo)

    if df.empty:
        print("El archivo está vacío.")
        return

    # ROI vs precio de venta ajustado
    plt.figure(figsize=(10, 6))
    plt.scatter(df["precio_venta_kg_ajustado"], df["roi"])
    plt.xlabel("Precio venta kg ajustado")
    plt.ylabel("ROI")
    plt.title("ROI vs precio de venta ajustado")
    plt.tight_layout()
    plt.show()

    # Utilidad vs peso de venta ajustado
    plt.figure(figsize=(10, 6))
    plt.scatter(df["peso_venta_kg_ajustado"], df["utilidad"])
    plt.xlabel("Peso venta kg ajustado")
    plt.ylabel("Utilidad")
    plt.title("Utilidad vs peso de venta ajustado")
    plt.tight_layout()
    plt.show()

    # ROI vs costo de pasto ajustado
    plt.figure(figsize=(10, 6))
    plt.scatter(df["costo_pasto_mensual_ajustado"], df["roi"])
    plt.xlabel("Costo pasto mensual ajustado")
    plt.ylabel("ROI")
    plt.title("ROI vs costo de pasto mensual ajustado")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    graficar_sensibilidad("outputs/sensibilidad_escenario_base.xlsx")