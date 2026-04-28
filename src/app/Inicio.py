import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st

ruta_logo = ROOT / "imagen" / "ChatGPT Image 10 abr 2026, 09_39_54.png"

st.set_page_config(page_title="LaCow", page_icon="🐄", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #eef2f7 0%, #e6edf5 100%);
    }

    .hero {
        background: linear-gradient(90deg, #0f172a, #1e3a5f);
        border-radius: 24px;
        padding: 28px;
        color: white;
        box-shadow: 0 18px 40px rgba(0,0,0,0.18);
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.4rem;
        font-weight: 800;
    }

    .hero p {
        margin-top: 0.6rem;
        color: #dbeafe;
        font-size: 1rem;
    }

    .card {
        background: white;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.08);
        border: 1px solid #dbe4ee;
        margin-bottom: 1rem;
    }

    .card h3 {
        margin: 0 0 0.4rem 0;
        color: #111827;
    }

    .card p {
        color: #6b7280;
        margin-bottom: 0;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 18px;
        padding: 14px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.06);
        border: 1px solid #dbe4ee;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns([1.3, 5], vertical_alignment="center")

with c1:
    if ruta_logo.exists():
        st.image(str(ruta_logo), width=180)

with c2:
    st.markdown(
        """
        <div class="hero">
            <h1>LaCow</h1>
            <p>Plataforma para simulación, inversión y gestión ganadera.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Módulos activos", "4")
with m2:
    st.metric("Estado", "Operativo")
with m3:
    st.metric("Enfoque", "Ganado + Analítica")

t1, t2 = st.columns(2)

with t1:
    st.markdown(
        """
        <div class="card">
            <h3>Invertir en ganado</h3>
            <p>Explora fincas, conoce la oferta de terneros y revisa oportunidades de inversión o compra directa.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Usa el menú lateral para entrar a **Invertir en ganado**.")

with t2:
    st.markdown(
        """
        <div class="card">
            <h3>Mi ganado</h3>
            <p>Registra animales, consulta inventario y organiza información operativa básica.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Usa el menú lateral para entrar a **Mi ganado**.")

st.markdown(
    """
    <div class="card">
        <h3>Qué encontrarás en LaCow</h3>
        <p>
        • Invertir en ganado<br>
        • Mi ganado<br>
        • Histórico y análisis<br>
        • Simulación financiera<br>
        • Comparación de escenarios
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)