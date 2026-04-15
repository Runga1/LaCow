import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st

from src.models.simulador_ganado import EscenarioGanado, calcular_rentabilidad
from src.utils.guardar_simulacion import guardar_simulacion_excel


# --------------------------------------------------
# FUNCION PARA COMPARADOR
# --------------------------------------------------
def construir_escenario(nombre: str, defaults: dict) -> dict:
    st.markdown(f"### {nombre}")

    peso_compra_kg = st.number_input(
        f"{nombre} - Peso compra",
        value=float(defaults["peso_compra_kg"]),
        key=f"{nombre}_1"
    )
    precio_compra_kg = st.number_input(
        f"{nombre} - Precio compra",
        value=float(defaults["precio_compra_kg"]),
        key=f"{nombre}_2"
    )
    peso_venta_kg = st.number_input(
        f"{nombre} - Peso venta",
        value=float(defaults["peso_venta_kg"]),
        key=f"{nombre}_3"
    )
    precio_venta_kg = st.number_input(
        f"{nombre} - Precio venta",
        value=float(defaults["precio_venta_kg"]),
        key=f"{nombre}_4"
    )
    costo_pasto_mensual = st.number_input(
        f"{nombre} - Pasto",
        value=float(defaults["costo_pasto_mensual"]),
        key=f"{nombre}_5"
    )
    costo_sal_med_mensual = st.number_input(
        f"{nombre} - Medicamentos",
        value=float(defaults["costo_sal_med_mensual"]),
        key=f"{nombre}_6"
    )
    meses = st.number_input(
        f"{nombre} - Meses",
        value=int(defaults["meses"]),
        key=f"{nombre}_7"
    )
    otros_costos = st.number_input(
        f"{nombre} - Otros",
        value=float(defaults["otros_costos"]),
        key=f"{nombre}_8"
    )

    return {
        "peso_compra_kg": peso_compra_kg,
        "precio_compra_kg": precio_compra_kg,
        "peso_venta_kg": peso_venta_kg,
        "precio_venta_kg": precio_venta_kg,
        "costo_pasto_mensual": costo_pasto_mensual,
        "costo_sal_med_mensual": costo_sal_med_mensual,
        "meses": int(meses),
        "otros_costos": otros_costos,
    }


# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="LaCow", layout="wide")

ruta_logo = ROOT / "imagen" / "ChatGPT Image 10 abr 2026, 09_39_54.png"
ruta_historico = ROOT / "outputs" / "historico_simulaciones.xlsx"

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #eef2f7 0%, #e6edf5 100%);
}

.brand-wrap {
    background: linear-gradient(90deg, #0f172a, #1e3a5f);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.brand-title {
    color: white;
    font-size: 2rem;
    font-weight: 800;
}

.brand-subtitle {
    color: #cbd5f5;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.stButton>button {
    background: linear-gradient(90deg,#16a34a,#22c55e);
    color:white;
    border-radius:12px;
    height:50px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER (ARREGLADO)
# --------------------------------------------------
logo_col, header_col = st.columns([2.5, 7.5])

with logo_col:
    st.markdown('<div style="display:flex; justify-content:center;">', unsafe_allow_html=True)
    st.image(str(ruta_logo), width=180)
    st.markdown('</div>', unsafe_allow_html=True)

with header_col:
    st.markdown("""
    <div class="brand-wrap">
        <div class="brand-title">LaCow</div>
        <div class="brand-subtitle">
        Simulador ganadero con enfoque en utilidad, ROI y punto de equilibrio
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Simulador", "Histórico", "Comparador"])

# ==================================================
# SIMULADOR
# ==================================================
with tab1:

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="card"><b>Datos del escenario</b></div>', unsafe_allow_html=True)

        peso_compra_kg = st.number_input("Peso compra", value=160.0)
        precio_compra_kg = st.number_input("Precio compra", value=7500.0)
        peso_venta_kg = st.number_input("Peso venta", value=450.0)
        precio_venta_kg = st.number_input("Precio venta", value=9200.0)
        costo_pasto_mensual = st.number_input("Pasto", value=60000.0)
        costo_sal_med_mensual = st.number_input("Medicamentos", value=15000.0)
        meses = st.number_input("Meses", value=12)
        otros_costos = st.number_input("Otros", value=100000.0)

        calcular = st.button("Calcular")

    with c2:
        st.markdown('<div class="card"><b>Resultados</b></div>', unsafe_allow_html=True)

        if calcular:

            datos = {
                "peso_compra_kg": peso_compra_kg,
                "precio_compra_kg": precio_compra_kg,
                "peso_venta_kg": peso_venta_kg,
                "precio_venta_kg": precio_venta_kg,
                "costo_pasto_mensual": costo_pasto_mensual,
                "costo_sal_med_mensual": costo_sal_med_mensual,
                "meses": int(meses),
                "otros_costos": otros_costos,
            }

            escenario = EscenarioGanado(**datos)
            res = calcular_rentabilidad(escenario)

            guardar_simulacion_excel(datos, res, "outputs/historico_simulaciones.xlsx")

            st.metric("Utilidad", f"${res['utilidad']:,.0f}")
            st.metric("ROI", f"{res['roi']:.2%}")
            st.metric("Equilibrio", f"${res['precio_equilibrio_kg_venta']:,.0f}")

# ==================================================
# HISTORICO
# ==================================================
with tab2:

    st.markdown('<div class="card"><b>Histórico</b></div>', unsafe_allow_html=True)

    if ruta_historico.exists():
        df = pd.read_excel(ruta_historico)
        st.dataframe(df)

# ==================================================
# COMPARADOR
# ==================================================
with tab3:

    st.markdown('<div class="card"><b>Comparador</b></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    defaults = {
        "peso_compra_kg":160,
        "precio_compra_kg":7500,
        "peso_venta_kg":450,
        "precio_venta_kg":9200,
        "costo_pasto_mensual":60000,
        "costo_sal_med_mensual":15000,
        "meses":12,
        "otros_costos":100000
    }

    with c1:
        esc1 = construir_escenario("Escenario 1", defaults)
    with c2:
        esc2 = construir_escenario("Escenario 2", defaults)
    with c3:
        esc3 = construir_escenario("Escenario 3", defaults)

    if st.button("Comparar"):

        resultados = []
        for nombre, esc in zip(["E1","E2","E3"], [esc1, esc2, esc3]):
            r = calcular_rentabilidad(EscenarioGanado(**esc))
            resultados.append({"escenario":nombre, **r})

        df = pd.DataFrame(resultados)
        st.dataframe(df)