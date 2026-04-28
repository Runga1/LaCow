import sys
from pathlib import Path
from urllib.parse import quote

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

if "usuario_logueado" not in st.session_state:
    st.session_state.usuario_logueado = False
if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = ""


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
        Plataforma de inversión ganadera colaborativa: compra, sostenimiento y reparto de utilidades
        </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.title("Navegación")
seccion = st.sidebar.radio(
    "Ir a",
    ["Inicio", "¿Qué es LaCow?", "Fincas disponibles", "Simulador financiero"],
)

if st.session_state.usuario_logueado:
    st.sidebar.success(f"Sesión activa: {st.session_state.nombre_usuario}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario_logueado = False
        st.session_state.nombre_usuario = ""
        st.rerun()


# ==================================================
# INICIO (REGISTRO / LOGIN)
# ==================================================
if seccion == "Inicio":
    st.markdown("## Bienvenido a LaCow")
    st.write("Regístrate o inicia sesión para empezar a explorar oportunidades ganaderas.")

    col_registro, col_login = st.columns(2)

    with col_registro:
        st.markdown('<div class="card"><b>Crear cuenta</b></div>', unsafe_allow_html=True)
        with st.form("form_registro"):
            nombre = st.text_input("Nombre completo")
            correo = st.text_input("Correo electrónico")
            telefono = st.text_input("WhatsApp")
            clave = st.text_input("Contraseña", type="password")
            aceptar = st.checkbox("Acepto términos y condiciones")
            crear_cuenta = st.form_submit_button("Registrarme")

            if crear_cuenta:
                if not all([nombre, correo, telefono, clave]) or not aceptar:
                    st.error("Completa todos los campos y acepta los términos.")
                else:
                    st.success(
                        "¡Registro exitoso! Tu cuenta quedó creada en modo demo. "
                        "Ahora puedes iniciar sesión."
                    )

    with col_login:
        st.markdown('<div class="card"><b>Iniciar sesión</b></div>', unsafe_allow_html=True)
        with st.form("form_login"):
            correo_login = st.text_input("Correo", key="correo_login")
            clave_login = st.text_input("Contraseña", type="password", key="clave_login")
            btn_login = st.form_submit_button("Entrar")

            if btn_login:
                if not correo_login or not clave_login:
                    st.error("Ingresa tu correo y contraseña.")
                else:
                    st.session_state.usuario_logueado = True
                    st.session_state.nombre_usuario = correo_login
                    st.success(f"Bienvenido, {correo_login}.")


# ==================================================
# INFORMACIÓN DE NEGOCIO
# ==================================================
elif seccion == "¿Qué es LaCow?":
    st.markdown("## ¿En qué consiste LaCow?")

    st.markdown(
        """
        <div class="card">
        <h4>Modelo de trabajo en campaña</h4>
        <p>
        LaCow conecta personas interesadas en invertir con ganaderos que sostienen el ganado en finca.
        El inversionista participa en la compra del ganado, el ganadero se encarga del sostenimiento,
        y al momento de la venta se reparten utilidades según el acuerdo (por ejemplo 60/40 o 50/50).
        </p>
        <ul>
          <li>Compra del ganado por lote o por cabeza.</li>
          <li>Sostenimiento por ganadero aliado en finca.</li>
          <li>Seguimiento de peso, costos y proyección de utilidad.</li>
          <li>Reparto de utilidades bajo porcentaje pactado.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Ejemplo de reparto")
    tabla_reparto = pd.DataFrame(
        {
            "Escenario": ["Utilidad total", "Inversionista 60%", "Ganadero 40%", "Inversionista 50%", "Ganadero 50%"],
            "Valor": ["$5.000.000", "$3.000.000", "$2.000.000", "$2.500.000", "$2.500.000"],
        }
    )
    st.table(tabla_reparto)


# ==================================================
# FINCAS DISPONIBLES
# ==================================================
elif seccion == "Fincas disponibles":
    st.markdown("## Fincas y ganado disponible")

    fincas = [
        {
            "nombre": "Finca El Encanto",
            "ubicacion": "Montería, Córdoba",
            "tipo": "Levante",
            "ganado": 36,
            "precio_estimado": "$1.350.000 por cabeza",
            "contacto": "+573001112233",
            "correo": "comercial@lacow.co",
        },
        {
            "nombre": "Hacienda San Pedro",
            "ubicacion": "Sincelejo, Sucre",
            "tipo": "Ceba",
            "ganado": 52,
            "precio_estimado": "$1.600.000 por cabeza",
            "contacto": "+573004445566",
            "correo": "asesor@lacow.co",
        },
        {
            "nombre": "Finca La Esperanza",
            "ubicacion": "Yopal, Casanare",
            "tipo": "Cría",
            "ganado": 24,
            "precio_estimado": "$1.250.000 por cabeza",
            "contacto": "+573007778899",
            "correo": "inversiones@lacow.co",
        },
    ]

    for idx, finca in enumerate(fincas):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(finca["nombre"])
        st.write(f"📍 Ubicación: {finca['ubicacion']}")
        st.write(f"🐄 Tipo de operación: {finca['tipo']}")
        st.write(f"✅ Ganado disponible: {finca['ganado']} cabezas")
        st.write(f"💰 Precio estimado: {finca['precio_estimado']}")

        mensaje = quote(
            f"Hola LaCow, estoy interesado en {finca['nombre']} ({finca['ganado']} cabezas disponibles)."
        )
        asunto = quote(f"Interés en {finca['nombre']}")
        cuerpo = quote(
            f"Quiero recibir información sobre {finca['nombre']}, ubicado en {finca['ubicacion']}."
        )
        whatsapp_url = f"https://wa.me/{finca['contacto'].replace('+', '')}?text={mensaje}"
        mailto_url = f"mailto:{finca['correo']}?subject={asunto}&body={cuerpo}"

        col_wpp, col_mail = st.columns(2)
        with col_wpp:
            st.link_button("Contactar por WhatsApp", whatsapp_url, key=f"wpp_{idx}")
        with col_mail:
            st.link_button("Enviar correo", mailto_url, key=f"mail_{idx}")

        st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# SIMULADOR FINANCIERO (MÓDULO EXISTENTE)
# ==================================================
else:
    tab1, tab2, tab3 = st.tabs(["Simulador", "Histórico", "Comparador"])

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

    with tab2:

        st.markdown('<div class="card"><b>Histórico</b></div>', unsafe_allow_html=True)

        if ruta_historico.exists():
            df = pd.read_excel(ruta_historico)
            st.dataframe(df)

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

        if st.button("Comparar"):

            resultados = []
            for nombre, esc in zip(["E1", "E2", "E3"], [esc1, esc2, esc3]):
                r = calcular_rentabilidad(EscenarioGanado(**esc))
                resultados.append({"escenario": nombre, **r})

            df = pd.DataFrame(resultados)
            st.dataframe(df)
