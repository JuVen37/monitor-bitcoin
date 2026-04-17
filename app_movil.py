import streamlit as st
import pandas as pd
import time
import requests

# 1. Configuración de la página (esto ayuda a que se vea bien en el móvil)
st.set_page_config(page_title="IA Juan Móvil", page_icon="📈", layout="centered")

st.title("🚀 Mi IA de Mercado")

def obtener_precio_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        return float(datos.get('bitcoin', {}).get('usd', 0))
    except:
        return 0

if 'historial' not in st.session_state:
    st.session_state.historial = [obtener_precio_crypto()]

# Contenedor principal que se refresca
placeholder = st.empty()

while True:
    nuevo_precio = obtener_precio_crypto()
    if nuevo_precio == 0:
        nuevo_precio = st.session_state.historial[-1]
    
    precio_anterior = st.session_state.historial[-1]
    st.session_state.historial.append(nuevo_precio)
    
    if len(st.session_state.historial) > 30:
        st.session_state.historial.pop(0)
    
    with placeholder.container():
        # --- AQUÍ EMPIEZA EL ORDEN NUEVO ---
        
        # Creamos 2 columnas: una para el precio y otra para la hora
        col1, col2 = st.columns(2)
        
        with col1:
            # st.metric crea ese diseño de "tablero de bolsa" con flechas
            st.metric(
                label="Bitcoin (USD) 🪙", 
                value=f"${nuevo_precio:,.2f}", 
                delta=f"${nuevo_precio - precio_anterior:,.2f}"
            )
        
        with col2:
            st.write("⏱️ **Última actualización**")
            st.info(time.strftime('%H:%M:%S'))
        
        # Un separador visual
        st.divider()
        
        # La gráfica ocupa todo el ancho abajo
        st.subheader("Evolución en tiempo real")
        st.line_chart(st.session_state.historial)
        
    time.sleep(15)
