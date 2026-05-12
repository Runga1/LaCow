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
        .stApp {
            background: radial-gradient(circle at 20% 10%, #0b1f38 0%, #0f243f 35%, #eaf0f7 35.2%, #eef3f9 100%);
        }
        .hero {
            position: relative;
            min-height: 560px;
            border-radius: 28px;
            overflow: hidden;
            box-shadow: 0 30px 60px rgba(12, 23, 38, 0.35);
            margin-bottom: 2rem;
            animation: fadeIn .8s ease;
            background:
                linear-gradient(110deg, rgba(6, 16, 30, .92) 0%, rgba(6, 16, 30, .74) 42%, rgba(12, 20, 35, .45) 65%, rgba(22, 35, 58, .35) 100%),
                url('https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=1800&q=80');
            background-size: cover;
            background-position: center;
        }
        .hero-glow {
            position: absolute;
            width: 340px;
            height: 340px;
            right: -90px;
            top: -70px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(39, 238, 154, .45) 0%, rgba(39, 238, 154, .08) 45%, transparent 70%);
            filter: blur(1px);
            animation: floaty 5s ease-in-out infinite;
        }
        .hero-body {
            position: relative;
            z-index: 2;
            width: min(680px, 92%);
            padding: 3.4rem 2.8rem;
            color: #f8fbff;
        }
        .hero-kicker {
            letter-spacing: .09rem;
            text-transform: uppercase;
            font-size: .85rem;
            color: #9eeac7;
            font-weight: 600;
        }
        .hero-title {
            font-size: clamp(2rem, 5vw, 3.8rem);
            line-height: 1.05;
            font-weight: 800;
            margin: .6rem 0 1rem 0;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #d8e4f2;
            margin-bottom: 1.4rem;
            max-width: 640px;
        }
        .hero-badges span {
            display: inline-block;
            margin-right: .5rem;
            margin-bottom: .5rem;
            padding: .35rem .75rem;
            border-radius: 999px;
            background: rgba(255,255,255,.12);
            border: 1px solid rgba(255,255,255,.22);
            font-size: .83rem;
        }
        .glass {
            background: rgba(255,255,255,.82);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(203, 213, 225, .9);
            border-radius: 22px;
            padding: 1.2rem 1.25rem;
            box-shadow: 0 16px 32px rgba(15, 23, 42, 0.11);
            animation: fadeUp .55s ease;
        }
        .glass h4 {
            margin: 0 0 .5rem 0;
            color: #111827;
        }
        .section-title {
            color: #0f172a;
            font-size: 1.75rem;
            margin: 1.1rem 0 .7rem 0;
            font-weight: 750;
        }
        .section-copy {
            color: #334155;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes floaty {
            0%,100% { transform: translateY(0px); }
            50% { transform: translateY(14px); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="hero">
            <div class="hero-glow"></div>
            <div class="hero-body">
                <div class="hero-kicker">LaCow · inversión ganadera inteligente</div>
                <div class="hero-title">Contratos al partir con trazabilidad y claridad financiera</div>
                <div class="hero-subtitle">
                    Conectamos inversionistas y tenedores para desarrollar ciclos ganaderos con reglas claras,
                    seguimiento operativo y liquidaciones transparentes.
                </div>
                <div class="hero-badges">
                    <span>Modelo aparcería</span>
                    <span>Acuerdos 50/50 · 60/40</span>
                    <span>Gestión de riesgo</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Acceso a la plataforma")
    st.markdown("<div class='section-copy'>Ingresa o crea tu cuenta para administrar tus operaciones y revisar el simulador.</div>", unsafe_allow_html=True)

    col_registro, col_login = st.columns(2, gap="large")

    with col_registro:
        st.markdown('<div class="glass"><h4>Crear cuenta</h4></div>', unsafe_allow_html=True)
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

    with col_login:
        st.markdown('<div class="glass"><h4>Iniciar sesión</h4></div>', unsafe_allow_html=True)
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
                    msg = "Bienvenido."
                    if recordar:
                        msg += " Dejaremos tu sesión recordada en este navegador (demo)."
                    st.success(msg)

    st.info("La sección de fincas y oferta de ganado continúa en el módulo lateral **Invertir en ganado** (sin duplicar información aquí).")

    st.markdown("<div class='section-title'>¿En qué consiste LaCow?</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="glass">
            <p>
            LaCow opera bajo contratos al partir (aparcería): una parte aporta ganado/capital y otra aporta tierra,
            manejo y operación. Al cierre del ciclo se liquidan resultados y se reparten utilidades según lo pactado.
            </p>
            <ul>
                <li>Marco de referencia en Colombia: Ley 6 de 1975 y Decreto 2815 de 1975.</li>
                <li>La valoración puede pactarse por kilos, valor de mercado, edad o modelo mixto.</li>
                <li>El reparto se define por contrato: 50/50, 55/45, 60/40, etc.</li>
                <li>Debe incluir cláusulas de mortalidad, fletes, vacunación y liquidación anticipada.</li>
                <li>La trazabilidad por animal (peso e identificación) evita conflictos de liquidación.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### Ejemplo práctico (liquidación anual)")
    st.table(
        pd.DataFrame(
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
    )

    st.markdown("<div class='section-title'>Simulador financiero</div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Simulador", "Histórico", "Comparador"])

    with tab1:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="glass"><h4>Datos del escenario</h4></div>', unsafe_allow_html=True)
            peso_compra_kg = st.number_input("Peso compra", value=160.0)
            precio_compra_kg = st.number_input("Precio compra", value=7500.0)
            peso_venta_kg = st.number_input("Peso venta", value=450.0)
            precio_venta_kg = st.number_input("Precio venta", value=9200.0)
            costo_pasto_mensual = st.number_input("Pasto", value=60000.0)
            costo_sal_med_mensual = st.number_input("Medicamentos", value=15000.0)
            meses = st.number_input("Meses", value=12)
            otros_costos = st.number_input("Otros", value=100000.0)
            calcular = st.button("Calcular")

        with col_b:
            st.markdown('<div class="glass"><h4>Resultados</h4></div>', unsafe_allow_html=True)
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
        st.markdown('<div class="glass"><h4>Histórico</h4></div>', unsafe_allow_html=True)
        if ruta_historico.exists():
            st.dataframe(pd.read_excel(ruta_historico), use_container_width=True)
        else:
            st.info("Aún no hay histórico de simulaciones.")

    with tab3:
        st.markdown('<div class="glass"><h4>Comparador</h4></div>', unsafe_allow_html=True)
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


run_app()
