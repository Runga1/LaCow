import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st
import plotly.express as px

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

.stButton > button {
    background: linear-gradient(90deg, #16a34a, #22c55e);
    color: white;
    border-radius: 12px;
    height: 50px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
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
        else:
            st.info("Completa los campos y pulsa Calcular.")

# ==================================================
# HISTORICO
# ==================================================
with tab2:
    st.markdown('<div class="card"><b>Histórico</b></div>', unsafe_allow_html=True)

    if ruta_historico.exists():
        df = pd.read_excel(ruta_historico)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no existe histórico de simulaciones.")

# ==================================================
# COMPARADOR
# ==================================================
with tab3:
    st.markdown('<div class="card"><b>Comparador</b></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    defaults = {
        "peso_compra_kg": 160,
        "precio_compra_kg": 7500,
        "peso_venta_kg": 450,
        "precio_venta_kg": 9200,
        "costo_pasto_mensual": 60000,
        "costo_sal_med_mensual": 15000,
        "meses": 12,
        "otros_costos": 100000
    }

    with c1:
        esc1 = construir_escenario("Escenario 1", defaults)
    with c2:
        esc2 = construir_escenario("Escenario 2", defaults)
    with c3:
        esc3 = construir_escenario("Escenario 3", defaults)

    comparar = st.button("Comparar escenarios")

    if comparar:
        resultados_comparacion = []

        escenarios_dict = {
            "Conservador": esc1,
            "Base": esc2,
            "Optimista": esc3,
        }

        for nombre, datos in escenarios_dict.items():
            escenario = EscenarioGanado(**datos)
            resultado = calcular_rentabilidad(escenario)

            resultados_comparacion.append({
                "escenario": nombre,
                **datos,
                **resultado
            })

        df_comparacion = pd.DataFrame(resultados_comparacion)

        st.markdown("### Comparación consolidada")
        st.dataframe(df_comparacion, use_container_width=True)

        m1, m2, m3 = st.columns(3)

        with m1:
            mejor_roi = df_comparacion.loc[df_comparacion["roi"].idxmax()]
            st.metric("Mejor ROI", mejor_roi["escenario"], f"{mejor_roi['roi']:.2%}")

        with m2:
            mayor_utilidad = df_comparacion.loc[df_comparacion["utilidad"].idxmax()]
            st.metric("Mayor utilidad", mayor_utilidad["escenario"], f"${mayor_utilidad['utilidad']:,.0f}")

        with m3:
            menor_equilibrio = df_comparacion.loc[df_comparacion["precio_equilibrio_kg_venta"].idxmin()]
            st.metric(
                "Menor precio equilibrio",
                menor_equilibrio["escenario"],
                f"${menor_equilibrio['precio_equilibrio_kg_venta']:,.2f}"
            )

        st.markdown("### Visualización comparativa")

        g1, g2 = st.columns(2)

        with g1:
            fig_utilidad = px.bar(
                df_comparacion,
                x="escenario",
                y="utilidad",
                title="Utilidad por escenario",
                text_auto=".2s",
            )
            fig_utilidad.update_layout(
                xaxis_title="Escenario",
                yaxis_title="Utilidad",
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            st.plotly_chart(fig_utilidad, use_container_width=True)

        with g2:
            fig_roi = px.bar(
                df_comparacion,
                x="escenario",
                y="roi",
                title="ROI por escenario",
                text_auto=".2%",
            )
            fig_roi.update_layout(
                xaxis_title="Escenario",
                yaxis_title="ROI",
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            st.plotly_chart(fig_roi, use_container_width=True)

        fig_equilibrio = px.bar(
            df_comparacion,
            x="escenario",
            y="precio_equilibrio_kg_venta",
            title="Precio de equilibrio por escenario",
            text_auto=".2f",
        )
        fig_equilibrio.update_layout(
            xaxis_title="Escenario",
            yaxis_title="Precio equilibrio kg venta",
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        st.plotly_chart(fig_equilibrio, use_container_width=True)