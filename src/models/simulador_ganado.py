from dataclasses import dataclass


@dataclass
class EscenarioGanado:
    peso_compra_kg: float
    precio_compra_kg: float
    peso_venta_kg: float
    precio_venta_kg: float
    costo_pasto_mensual: float
    costo_sal_med_mensual: float
    meses: int
    otros_costos: float = 0


def calcular_rentabilidad(escenario: EscenarioGanado):

    compra_total = escenario.peso_compra_kg * escenario.precio_compra_kg
    venta_total = escenario.peso_venta_kg * escenario.precio_venta_kg

    costo_sostenimiento = (
        escenario.costo_pasto_mensual + escenario.costo_sal_med_mensual
    ) * escenario.meses

    costo_total = compra_total + costo_sostenimiento + escenario.otros_costos

    utilidad = venta_total - costo_total

    roi = utilidad / costo_total if costo_total > 0 else 0

    return {
        "compra_total": compra_total,
        "venta_total": venta_total,
        "costo_sostenimiento": costo_sostenimiento,
        "costo_total": costo_total,
        "utilidad": utilidad,
        "roi": roi,
    }