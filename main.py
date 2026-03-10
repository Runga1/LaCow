from src.models.simulador_ganado import EscenarioGanado, calcular_rentabilidad
from src.utils.formatters import moneda, porcentaje


def main():

    escenario = EscenarioGanado(
        peso_compra_kg=180,
        precio_compra_kg=7800,
        peso_venta_kg=420,
        precio_venta_kg=9200,
        costo_pasto_mensual=60000,
        costo_sal_med_mensual=14000,
        meses=12,
        otros_costos=100000,
    )

    resultado = calcular_rentabilidad(escenario)

    print("\nSIMULADOR GANADERO\n")

    print("Compra total:", moneda(resultado["compra_total"]))
    print("Venta total:", moneda(resultado["venta_total"]))
    print("Costo sostenimiento:", moneda(resultado["costo_sostenimiento"]))
    print("Costo total:", moneda(resultado["costo_total"]))
    print("Utilidad:", moneda(resultado["utilidad"]))
    print("ROI:", porcentaje(resultado["roi"]))


if __name__ == "__main__":
    main()