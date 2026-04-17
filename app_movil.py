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
    try: requests.get(url)
    except: pass

# --- MOTOR DE DATOS REALES (ESIOS - RED ELÉCTRICA) ---
def obtener_luz_real():
    try:
        # Consultamos el precio de hoy (PVPC)
        url = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
        response = requests.get(url)
        datos = response.json()
        
        # Hora actual en España
        tz = pytz.timezone('Europe/Madrid')
        hora_actual = datetime.now(tz).strftime("%H") + "-24" # Formato de la API
        
        precio_ahora = datos[hora_actual]['price'] / 1000 # Convertir a €/kWh
        
        # Calcular media real del día
        todos_los_precios = [v['price'] for k, v in datos.items()]
        media_dia = (sum(todos_los_precios) / len(todos_los_precios)) / 1000
        
        diferencia = (precio_ahora - media_dia) / media_dia
        
        if diferencia < -0.15: estado = "🔥 ¡GANGA REAL!"
        elif diferencia < 0: estado = "🟢 Barato"
        else: estado = "🔴 Caro"
        
        return precio_ahora, estado, media_dia
    except:
        return 0.15, "⚠️ Error API", 0.15

def obtener_precio_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        r = requests.get(url)
        return float(r.json().get('bitcoin', {}).get('usd', 0))
    except: return 0

# --- INTERFAZ ---
st.set_page_config(page_title="IA Maestra Creal", page_icon="⚡", layout="wide")
st.title("⚡ IA Operativa: Datos de Red Eléctrica")

if 'ultima_notificacion' not in st.session_state:
    st.session_state.ultima_notificacion = 0

placeholder = st.empty()

while True:
    btc = obtener_precio_crypto()
    luz, etiqueta, media = obtener_luz_real()
    ahora_ts = time.time()
    
    with placeholder.container():
        c1, c2 = st.columns(2)
        c1.metric("LUZ REAL (ESPAÑA)", f"{luz:.4f} €/kWh", etiqueta)
        c1.caption(f"Media real de hoy: {media:.4f} €/kWh")
        c2.metric("BITCOIN", f"${btc:,.2f}")
        
        # LÓGICA DE AVISO REAL
        if etiqueta == "🔥 ¡GANGA REAL!" and (ahora_ts - st.session_state.ultima_notificacion > 3600):
            msj = f"⚡ ¡AVISO REAL! La luz en España está ahora a {luz:.4f}€ (Ganga). BTC a ${btc:,.2f}."
            enviar_aviso_telegram(msj)
            st.session_state.ultima_notificacion = ahora_ts
            st.success("📲 Notificación de mercado real enviada.")

        st.line_chart([btc-20, btc+10, btc])
    
    time.sleep(60) # Actualizamos cada minuto
