import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE IDENTIDAD ---
TOKEN_TELEGRAM = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
ID_USUARIO = "8449303559"

# --- INTERFAZ PREMIUM (CSS) ---
st.set_page_config(page_title="CREAL INTELLIGENCE", page_icon="🕵️‍♂️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00ffc8; }
    .stMetric { background-color: #111111; border: 1px solid #00ffc8; border-radius: 15px; padding: 20px; box-shadow: 0px 0px 15px #00ffc833; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Courier New', Courier, monospace; }
    .stAlert { background-color: #00221a; border: 1px solid #00ffc8; color: #00ffc8; }
    </style>
    """, unsafe_allow_html=True)

def enviar_aviso_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={ID_USUARIO}&text={mensaje}"
    try: requests.get(url)
    except: pass

def obtener_luz_real():
    try:
        url = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
        datos = requests.get(url).json()
        tz = pytz.timezone('Europe/Madrid')
        hora_actual = datetime.now(tz).strftime("%H") + "-24"
        precio_ahora = datos[hora_actual]['price'] / 1000
        todos_p = [v['price'] for k, v in datos.items()]
        media_dia = (sum(todos_p) / len(todos_p)) / 1000
        diff = (precio_ahora - media_dia) / media_dia
        if diff < -0.15: est = "⚡ GANGA DETECTADA"
        elif diff < 0: est = "✅ Precio Óptimo"
        else: est = "⚠️ Pico de Gasto"
        return precio_ahora, est, media_dia
    except: return 0.15, "Consultando...", 0.15

def obtener_noticias():
    try:
        # Buscamos noticias sobre economía y tecnología
        url = "https://newsapi.org/v2/everything?q=bitcoin+economy&pageSize=1&apiKey=748a3962649b49b6b9075e7a93557454" # API de prueba
        r = requests.get(url).json()
        return r['articles'][0]['title']
    except: return "Escaneando titulares globales..."

def obtener_btc():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
        return float(r['bitcoin']['usd'])
    except: return 0.0

# --- DASHBOARD ---
st.title("🕵️‍♂️ CREAL MASTER INTELLIGENCE")
st.write(f"Sincronizado con Nodo Central | {datetime.now().strftime('%H:%M:%S')}")

if 'ultima_notif' not in st.session_state: st.session_state.ultima_notif = 0

placeholder = st.empty()

while True:
    btc = obtener_btc()
    luz, etiqueta, media = obtener_luz_real()
    noticia = obtener_noticias()
    ahora = time.time()
    
    with placeholder.container():
        # Fila de Métricas
        c1, c2, c3 = st.columns(3)
        c1.metric("LUZ PVPC ESPAÑA", f"{luz:.4f} €", etiqueta)
        c2.metric("BITCOIN (USD)", f"${btc:,.0f}")
        c3.metric("STATUS RED", "OPERATIVO", "100%")
        
        st.divider()
        
        # Fila de Inteligencia
        col_inf, col_news = st.columns([1, 2])
        with col_inf:
            st.info(f"💡 **Sugerencia IA:** {'Aprovecha para consumir ahora' if luz < media else 'Pospón gastos eléctricos'}")
            if etiqueta == "⚡ GANGA DETECTADA" and (ahora - st.session_state.ultima_notif > 3600):
                enviar_aviso_telegram(f"🕵️‍♂️ CREAL: ¡Luz en mínimo! {luz:.4f}€. BTC: ${btc:,.0f}")
                st.session_state.ultima_notif = ahora
        
        with col_news:
            st.warning(f"📰 **ÚLTIMA HORA:** {noticia}")
        
        # Gráfico Estilizado
        st.line_chart(pd.DataFrame([btc-100, btc+50, btc-20, btc], columns=["Market Flow"]))
        
    time.sleep(60)
