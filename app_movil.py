import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE TU IA ---
TOKEN_TELEGRAM = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
ID_USUARIO = "8449303559"

def enviar_aviso_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={ID_USUARIO}&text={mensaje}"
    try:
        requests.get(url)
    except:
        pass

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="IA Maestra Creal", page_icon="🧠", layout="wide")

st.title("🧠 IA de Gestión Proactiva")
st.write(f"Conectado con el Bot: **CrealMasterIA_bot**")

def obtener_datos_luz():
    # Precios simulados para forzar la "Ganga" y que veas el mensaje en el móvil
    precios_dia = [0.12, 0.15, 0.18, 0.22, 0.25, 0.20, 0.14, 0.10, 0.08, 0.11, 0.13, 0.16]
    precio_actual = 0.07  # Forzamos precio bajo para el test
    media = sum(precios_dia) / len(precios_dia)
    diferencia = ((precio_actual - media) / media)
    
    if diferencia < -0.20:
        estado = "🔥 ¡GANGA TOTAL!"
    elif diferencia < 0:
        estado = "🟢 Barato"
    else:
        estado = "🔴 Caro"
    return precio_actual, estado, media

def obtener_precio_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        r = requests.get(url)
        return float(r.json().get('bitcoin', {}).get('usd', 0))
    except: return 0

# Para no saturar el móvil, solo avisamos una vez cada hora
if 'ultima_notificacion' not in st.session_state:
    st.session_state.ultima_notificacion = 0

placeholder = st.empty()

while True:
    btc = obtener_precio_crypto()
    luz, etiqueta, media = obtener_datos_luz()
    ahora = time.time()
    
    with placeholder.container():
        col1, col2 = st.columns(2)
        with col1:
            st.metric("LUZ ACTUAL", f"{luz} €/kWh", etiqueta)
            st.caption(f"Media diaria: {media:.2f} €/kWh")
        with col2:
            st.metric("BITCOIN", f"${btc:,.2f}")
        
        # --- EL CEREBRO DE TU IA ---
        if etiqueta == "🔥 ¡GANGA TOTAL!":
            # Si han pasado más de 60 minutos desde el último aviso
            if (ahora - st.session_state.ultima_notificacion > 3600):
                msj = f"🚀 ¡HOLA CREAL! Tu IA ha detectado una GANGA: Luz a {luz}€/kWh. BTC está a ${btc:,.2f}. ¡Aprovecha ahora!"
                enviar_aviso_telegram(msj)
                st.session_state.ultima_notificacion = ahora
                st.success("📲 ¡Aviso enviado a tu Telegram!")

        # Gráfico histórico simulado
        st.line_chart([btc-50, btc+20, btc-80, btc])
    
    time.sleep(30)
