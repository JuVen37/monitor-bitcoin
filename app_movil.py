import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
import pytz

# 1. Configuración de la "Nave"
st.set_page_config(page_title="IA Maestra Juan", page_icon="🧠", layout="wide")

# Estilo para que se vea premium
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 IA de Gestión Proactiva")
st.subheader("Tu Gemelo Digital analizando oportunidades...")

# 2. El Motor de la Luz (API simplificada para el ejemplo)
def obtener_datos_luz():
    # En un entorno real usaríamos la API de ESIOS, aquí simulamos la lógica "top"
    # Simulamos precios del día para calcular la media
    precios_dia = [0.12, 0.15, 0.18, 0.22, 0.25, 0.20, 0.14, 0.10, 0.08, 0.11, 0.13, 0.16]
    precio_actual = 0.11 # Esto vendría de la API según la hora
    media = sum(precios_dia) / len(precios_dia)
    
    diferencia = ((precio_actual - media) / media)
    
    if diferencia < -0.20:
        estado = "🔥 ¡GANGA TOTAL!"
        color = "inverse"
    elif diferencia < 0:
        estado = "🟢 Barato"
        color = "normal"
    else:
        estado = "🔴 Caro (Evitar gasto)"
        color = "off"
    
    return precio_actual, estado, media

# 3. El Motor de Cripto (Tu base original)
def obtener_precio_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        r = requests.get(url)
        return float(r.json().get('bitcoin', {}).get('usd', 0))
    except: return 0

# --- Lógica de Sesión ---
if 'historial_btc' not in st.session_state:
    st.session_state.historial_btc = [obtener_precio_crypto()]

placeholder = st.empty()

# 4. El Bucle de la Super-IA
while True:
    btc = obtener_precio_crypto()
    luz, etiqueta_luz, media_luz = obtener_datos_luz()
    
    with placeholder.container():
        # FILA 1: Los ojos de la IA
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("LUZ ACTUAL", f"{luz} €/kWh", etiqueta_luz)
            st.caption(f"Media del día: {media_luz:.2f} €/kWh")
            
        with col2:
            prev_btc = st.session_state.historial_btc[-1]
            diff_btc = btc - prev_btc
            st.metric("BITCOIN", f"${btc:,.2f}", f"{diff_btc:,.2f}$")
        
        st.divider()
        
        # FILA 2: El Cerebro (La parte que hace flipar a la gente)
        st.info("🤖 **Análisis del Gemelo Digital:**")
        
        if etiqueta_luz == "🔥 ¡GANGA TOTAL!" and diff_btc < 0:
            st.success("🎯 OPORTUNIDAD MAESTRA: La luz está regalada y el Bitcoin ha bajado. Es el momento ideal para mover ficha.")
        elif etiqueta_luz == "🔴 Caro (Evitar gasto)":
            st.warning("⚠️ SUGERENCIA: Desconecta dispositivos no esenciales. El precio de la energía no compensa el gasto ahora mismo.")
        else:
            st.write("🔎 Buscando anomalías en el mercado... Todo estable.")

        # Gráfica de Bitcoin
        st.session_state.historial_btc.append(btc)
        if len(st.session_state.historial_btc) > 20: st.session_state.historial_btc.pop(0)
        st.line_chart(st.session_state.historial_btc)

    time.sleep(15)
