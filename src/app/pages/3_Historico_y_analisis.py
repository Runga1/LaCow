import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Histórico y análisis", layout="wide")

ruta_historico = ROOT / "outputs" / "historico_simulaciones.xlsx"

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #eef2f7 0%, #e6edf5 100%);
    }

    .title-card {
        background: linear-gradient(90deg, #0f172a, #1e3a5f);
        color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 14px 30px rgba(0,0,0,0.16);
        margin-bottom: 1rem;
    }

    .card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
        border: 1px solid #dbe4ee;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="title-card">
        <h1>Histórico y análisis</h1>
        <p>Consulta las simulaciones guardadas y revisa indicadores básicos.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not ruta_historico.exists():
    st.warning("Aún no existe histórico de simulaciones.")
    st.stop()

df_hist = pd.read_excel(ruta_historico)

if df_hist.empty:
    st.info("El histórico existe, pero está vacío.")
    st.stop()

st.markdown('<div class="card"><h3>Simulaciones guardadas</h3></div>', unsafe_allow_html=True)
st.dataframe(df_hist, use_container_width=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Simulaciones", len(df_hist))

with c2:
    st.metric("ROI promedio", f"{df_hist['roi'].mean():.2%}")

with c3:
    st.metric("Utilidad promedio", f"${df_hist['utilidad'].mean():,.0f}")

top_roi = df_hist.sort_values(by="roi", ascending=False).head(5)

st.markdown('<div class="card"><h3>Top 5 simulaciones por ROI</h3></div>', unsafe_allow_html=True)
st.dataframe(top_roi, use_container_width=True)