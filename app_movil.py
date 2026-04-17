import streamlit as st
import pandas as pd
import time
import requests

# 1. Configuración de la interfaz
st.set_page_config(page_title="IA Juan Móvil", page_icon="📈")
st.title("🚀 Mi IA de Mercado")

# 2. Definición del "Motor" (La función que faltaba)
def obtener_precio_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        return float(datos.get('bitcoin', {}).get('usd', 0))
    except:
        return 0

# 3. Preparación de la memoria
if 'historial' not in st.session_state:
    st.session_state.historial = [obtener_precio_crypto()]

placeholder = st.empty()

# 4. Bucle de trabajo
while True:
    nuevo_precio = obtener_precio_crypto()
    
    # Si la API falla, mantenemos el último precio para no romper la gráfica
    if nuevo_precio == 0:
        nuevo_precio = st.session_state.historial[-1]
    
    precio_anterior = st.session_state.historial[-1]
    st.session_state.historial.append(nuevo_precio)
    
    if len(st.session_state.historial) > 30:
        st.session_state.historial.pop(0)
    
    with placeholder.container():
        st.metric("Bitcoin (USD)", f"${nuevo_precio:,.2f}", f"{nuevo_precio - precio_anterior:,.2f}")
        st.line_chart(st.session_state.historial)
    
    time.sleep(15) # Un respiro de 15 segundos para no cansar a la API
