import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mi ganado", layout="wide")

ruta_ganado = ROOT / "src" / "data" / "app_data" / "ganado_propietario.xlsx"

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
        <h1>Mi ganado</h1>
        <p>Registra y consulta los animales que ya tienes para llevar control básico.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if ruta_ganado.exists():
    df_ganado = pd.read_excel(ruta_ganado)
else:
    df_ganado = pd.DataFrame(columns=[
        "id_animal",
        "raza",
        "sexo",
        "fecha_compra",
        "peso_compra_kg",
        "precio_compra_kg",
        "precio_compra_total",
        "finca",
        "estado",
        "observaciones",
    ])

st.markdown('<div class="card"><h3>Registrar animal</h3></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    id_animal = st.text_input("ID del animal")
    raza = st.text_input("Raza")
    sexo = st.selectbox("Sexo", ["Macho", "Hembra"])
    fecha_compra = st.date_input("Fecha de compra")
    peso_compra_kg = st.number_input("Peso de compra (kg)", min_value=0.0, value=180.0)

with c2:
    precio_compra_kg = st.number_input("Precio de compra por kg", min_value=0.0, value=7500.0)
    finca = st.text_input("Finca")
    estado = st.selectbox("Estado", ["Activo", "Vendido", "En engorde"])
    observaciones = st.text_area("Observaciones")

if st.button("Guardar animal"):
    precio_compra_total = peso_compra_kg * precio_compra_kg

    nueva_fila = pd.DataFrame([{
        "id_animal": id_animal,
        "raza": raza,
        "sexo": sexo,
        "fecha_compra": fecha_compra,
        "peso_compra_kg": peso_compra_kg,
        "precio_compra_kg": precio_compra_kg,
        "precio_compra_total": precio_compra_total,
        "finca": finca,
        "estado": estado,
        "observaciones": observaciones,
    }])

    df_ganado = pd.concat([df_ganado, nueva_fila], ignore_index=True)
    ruta_ganado.parent.mkdir(parents=True, exist_ok=True)
    df_ganado.to_excel(ruta_ganado, index=False)

    st.success("Animal guardado correctamente.")

st.markdown('<div class="card"><h3>Inventario actual</h3></div>', unsafe_allow_html=True)

if df_ganado.empty:
    st.info("Aún no hay animales registrados.")
else:
    st.dataframe(df_ganado, use_container_width=True)