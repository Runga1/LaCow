import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Invertir en ganado", layout="wide")

ruta_fincas = ROOT / "src" / "data" / "app_data" / "fincas.xlsx"
ruta_razas = ROOT / "src" / "data" / "app_data" / "razas.xlsx"
ruta_imagenes = ROOT / "imagen"

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
        <h1>Invertir en ganado</h1>
        <p>Explora fincas disponibles y conoce la oferta de terneros.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not ruta_fincas.exists():
    st.error(f"No se encontró el archivo de fincas en: {ruta_fincas}")
    st.stop()

if not ruta_razas.exists():
    st.error(f"No se encontró el archivo de razas en: {ruta_razas}")
    st.stop()

df_fincas = pd.read_excel(ruta_fincas)
df_razas = pd.read_excel(ruta_razas)

if df_fincas.empty:
    st.warning("El archivo de fincas está vacío.")
    st.stop()

finca_seleccionada = st.selectbox(
    "Selecciona una finca",
    df_fincas["nombre_finca"].tolist()
)

finca = df_fincas[df_fincas["nombre_finca"] == finca_seleccionada].iloc[0]
razas_finca = df_razas[df_razas["id_finca"] == finca["id_finca"]]

c1, c2 = st.columns([1.1, 1])

with c1:
    st.markdown(
        f"""
        <div class="card">
            <h2>{finca['nombre_finca']}</h2>
            <p><b>Departamento:</b> {finca['departamento']}</p>
            <p><b>Municipio:</b> {finca['municipio']}</p>
            <p><b>Localidad:</b> {finca['localidad']}</p>
            <p><b>Clima:</b> {finca['clima']}</p>
            <p><b>Tipo de operación:</b> {finca['tipo_operacion']}</p>
            <p><b>Descripción:</b> {finca['descripcion']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    ruta_foto_finca = ruta_imagenes / str(finca["imagen_finca"])
    if ruta_foto_finca.exists():
        st.image(str(ruta_foto_finca), use_container_width=True)
    else:
        st.info("No se encontró la imagen de la finca.")

st.subheader("Oferta disponible")

if razas_finca.empty:
    st.warning("No hay razas o terneros cargados para esta finca.")
else:
    for _, raza in razas_finca.iterrows():
        r1, r2 = st.columns([1, 1.2])

    descripcion_raza = raza["descripcion"] if "descripcion" in raza.index else "Sin descripción registrada"

    with r1:
        ruta_foto_raza = ruta_imagenes / str(raza["imagen_raza"])
        if ruta_foto_raza.exists():
            st.image(str(ruta_foto_raza), use_container_width=True)
        else:
            st.info("No se encontró la imagen del ternero/raza.")

    with r2:
        st.markdown(
            f"""
            <div class="card">
                <h3>{raza['raza']}</h3>
                <p><b>Tipo de animal:</b> {raza['tipo_animal']}</p>
                <p><b>Rango de peso:</b> {raza['rango_peso']}</p>
                <p><b>Precio estimado:</b> ${raza['precio_estimado']:,.0f}</p>
                <p><b>Cantidad disponible:</b> {raza['cantidad_disponible']}</p>
                <p><b>Descripción:</b> {descripcion_raza}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(f"Quiero información de {raza['raza']}", key=f"btn_{raza['id_raza']}"):
            st.success(
                f"Has mostrado interés en {raza['raza']} de la finca {finca['nombre_finca']}."
            )