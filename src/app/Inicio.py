import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.models.simulador_ganado import EscenarioGanado, calcular_rentabilidad
from src.utils.guardar_simulacion import guardar_simulacion_excel


def construir_escenario(nombre: str, defaults: dict) -> dict:
    st.markdown(f"### {nombre}")

    peso_compra_kg = st.number_input(f"{nombre} - Peso compra", value=float(defaults["peso_compra_kg"]), key=f"{nombre}_1")
    precio_compra_kg = st.number_input(f"{nombre} - Precio compra", value=float(defaults["precio_compra_kg"]), key=f"{nombre}_2")
    peso_venta_kg = st.number_input(f"{nombre} - Peso venta", value=float(defaults["peso_venta_kg"]), key=f"{nombre}_3")
    precio_venta_kg = st.number_input(f"{nombre} - Precio venta", value=float(defaults["precio_venta_kg"]), key=f"{nombre}_4")
    costo_pasto_mensual = st.number_input(f"{nombre} - Pasto", value=float(defaults["costo_pasto_mensual"]), key=f"{nombre}_5")
    costo_sal_med_mensual = st.number_input(f"{nombre} - Medicamentos", value=float(defaults["costo_sal_med_mensual"]), key=f"{nombre}_6")
    meses = st.number_input(f"{nombre} - Meses", value=int(defaults["meses"]), key=f"{nombre}_7")
    otros_costos = st.number_input(f"{nombre} - Otros", value=float(defaults["otros_costos"]), key=f"{nombre}_8")

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


def run_app() -> None:
    st.set_page_config(page_title="LaCow", page_icon="🐄", layout="wide")

    ruta_logo = ROOT / "imagen" / "ChatGPT Image 10 abr 2026, 09_39_54.png"
    ruta_historico = ROOT / "outputs" / "historico_simulaciones.xlsx"

    if "usuario_logueado" not in st.session_state:
        st.session_state.usuario_logueado = False
    if "nombre_usuario" not in st.session_state:
        st.session_state.nombre_usuario = ""

    st.markdown(
        """
    <style>
    .stApp { background: linear-gradient(180deg, #f4f7fb 0%, #eaf1f8 100%); }
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        border-radius: 24px;
        padding: 32px;
        color: white;
        box-shadow: 0 20px 45px rgba(10, 20, 40, .25);
        animation: fadeUp .6s ease;
    }
    .hero::before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        background: rgba(255,255,255,.08);
        top: -80px;
        right: -40px;
    }
    .section-card {
        background: #fff;
        border-radius: 20px;
        padding: 22px;
        border: 1px solid #dbe4ee;
        box-shadow: 0 10px 24px rgba(0,0,0,.06);
        animation: fadeUp .55s ease;
    }
    .section-card:hover { transform: translateY(-2px); transition: .25s ease; }
    .lacow-chip {
        display: inline-block;
        padding: .28rem .65rem;
        border-radius: 999px;
        font-size: .83rem;
        background: #dbeafe;
        color: #1e3a8a;
        margin-right: .4rem;
        margin-bottom: .4rem;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    logo_col, hero_col = st.columns([1.6, 8.4], vertical_alignment="center")
    with logo_col:
        if ruta_logo.exists():
            st.image(str(ruta_logo), width=170)

    with hero_col:
        st.markdown(
            """
            <div class="hero">
                <h1 style="margin:0;font-size:2.2rem;">Bienvenido a LaCow</h1>
                <p style="margin:.8rem 0 0 0;color:#dbeafe;font-size:1.05rem;max-width:900px;">
                    Plataforma para invertir en ganadería bajo contratos al partir,
                    con trazabilidad, acuerdos claros y proyección financiera.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab_inicio, tab_info, tab_sim = st.tabs(["Inicio", "¿Qué es LaCow?", "Simulador financiero"])

    with tab_inicio:
        st.markdown("#### Acceso a la plataforma")

        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("##### Crear cuenta")
            with st.form("form_registro"):
                nombre = st.text_input("Nombre completo", placeholder="Ej: Juan David Pérez")
                correo = st.text_input("Correo electrónico", placeholder="correo@ejemplo.com")
                telefono = st.text_input("WhatsApp", placeholder="+57 300 000 0000")
                ciudad = st.text_input("Ciudad", placeholder="Montería")
                clave = st.text_input("Contraseña", type="password")
                confirmar_clave = st.text_input("Confirmar contraseña", type="password")
                aceptar = st.checkbox("Acepto términos y política de tratamiento de datos")
                crear_cuenta = st.form_submit_button("Registrarme")

                if crear_cuenta:
                    if not all([nombre, correo, telefono, ciudad, clave, confirmar_clave]):
                        st.error("Completa todos los campos del registro.")
                    elif clave != confirmar_clave:
                        st.error("Las contraseñas no coinciden.")
                    elif not aceptar:
                        st.error("Debes aceptar los términos para continuar.")
                    else:
                        st.success("Registro creado (modo demo). Ya puedes iniciar sesión.")
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("##### Iniciar sesión")
            with st.form("form_login"):
                correo_login = st.text_input("Correo", key="correo_login", placeholder="correo@ejemplo.com")
                clave_login = st.text_input("Contraseña", type="password", key="clave_login")
                recordar = st.checkbox("Recordar mi sesión")
                btn_login = st.form_submit_button("Entrar")

                if btn_login:
                    if not correo_login or not clave_login:
                        st.error("Ingresa correo y contraseña.")
                    else:
                        st.session_state.usuario_logueado = True
                        st.session_state.nombre_usuario = correo_login
                        mensaje = "Bienvenido."
                        if recordar:
                            mensaje += " Dejaremos tu sesión recordada en este navegador (demo)."
                        st.success(mensaje)
            st.markdown('</div>', unsafe_allow_html=True)

        st.info("Las fincas y oferta de ganado se administran desde el módulo **Invertir en ganado** en el menú lateral.")

    with tab_info:
        st.markdown("#### ¿En qué consiste LaCow?")
        st.markdown(
            """
            <div class="section-card">
                <span class="lacow-chip">Contrato al partir</span>
                <span class="lacow-chip">Aparcería ganadera</span>
                <span class="lacow-chip">Mutua colaboración</span>
                <p style="margin-top:.8rem;">
                LaCow opera bajo la lógica de contratos al partir (aparcería): una parte aporta ganado o capital,
                la otra aporta tierra, manejo, trabajo y operación. Al cierre del ciclo se liquidan resultados y
                se reparten utilidades conforme al acuerdo establecido por contrato.
                </p>
                <ul>
                    <li>Base legal en Colombia: Ley 6 de 1975 y Decreto 2815 de 1975.</li>
                    <li>Las partes definen reglas de valoración (kilos, dinero, edad o mezcla).</li>
                    <li>El reparto puede ser 50/50, 55/45, 60/40 u otra fórmula pactada.</li>
                    <li>Debe incluir manejo de mortalidad, fletes, vacunación y causales de liquidación anticipada.</li>
                    <li>La trazabilidad por animal (peso, identificación y movimientos) es clave para una liquidación justa.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Ejemplo práctico (liquidación anual)")
        ejemplo = pd.DataFrame(
            {
                "Concepto": [
                    "Valor inicial del lote",
                    "Valor al cierre del ciclo",
                    "Excedente / utilidad bruta",
                    "Reparto 50% propietario",
                    "Reparto 50% tenedor",
                ],
                "Valor": ["$75.000.000", "$172.000.000", "$97.000.000", "$48.500.000", "$48.500.000"],
            }
        )
        st.table(ejemplo)

        st.warning(
            "Recomendación: en contratos al partir, pactar por escrito metodología de valoración, "
            "mortalidad asumida y costos operativos para evitar diferencias al liquidar."
        )

    with tab_sim:
        tab1, tab2, tab3 = st.tabs(["Simulador", "Histórico", "Comparador"])

        with tab1:
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("##### Datos del escenario")
                peso_compra_kg = st.number_input("Peso compra", value=160.0)
                precio_compra_kg = st.number_input("Precio compra", value=7500.0)
                peso_venta_kg = st.number_input("Peso venta", value=450.0)
                precio_venta_kg = st.number_input("Precio venta", value=9200.0)
                costo_pasto_mensual = st.number_input("Pasto", value=60000.0)
                costo_sal_med_mensual = st.number_input("Medicamentos", value=15000.0)
                meses = st.number_input("Meses", value=12)
                otros_costos = st.number_input("Otros", value=100000.0)
                calcular = st.button("Calcular")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_b:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("##### Resultados")

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
                    st.caption("Completa datos y pulsa Calcular para ver resultados.")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("##### Histórico")
            if ruta_historico.exists():
                st.dataframe(pd.read_excel(ruta_historico), use_container_width=True)
            else:
                st.info("Aún no hay histórico de simulaciones.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("##### Comparador")
            c1, c2, c3 = st.columns(3)
            defaults = {
                "peso_compra_kg": 160,
                "precio_compra_kg": 7500,
                "peso_venta_kg": 450,
                "precio_venta_kg": 9200,
                "costo_pasto_mensual": 60000,
                "costo_sal_med_mensual": 15000,
                "meses": 12,
                "otros_costos": 100000,
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
                st.dataframe(pd.DataFrame(resultados), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


run_app()
