import streamlit as st
import pandas as pd
import time
import requests

# 1. Configuración de la página
st.set_page_config(page_title="IA Juan Móvil", page_icon="📈", layout="centered")

st.title("🚀 Mi IA de Mercado")

# 2. Motor de datos (CoinGecko para evitar bloqueos)
def obtener_precio_crypto():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        return float(datos.get('bitcoin', {}).get('usd', 0))
    except:
        return 0

# 3. Inicialización del historial
if 'historial' not in st.session_state:
    precio_inicial = obtener_precio_crypto()
    st.session_state.historial = [precio_inicial] if precio_inicial > 0 else [0.0]

# Contenedor para la actualización en vivo
placeholder = st.empty()

# 4. Bucle principal
while True:
    nuevo_precio = obtener_precio_crypto()
    
    # Si la API falla, mantenemos el último precio conocido
    if nuevo_precio == 0:
        nuevo_precio = st.session_state.historial[-1]
    
    precio_anterior = st.session_state.historial[-1]
    st.session_state.historial.append(nuevo_precio)
    
    # Mantener solo los últimos 30 puntos
    if len(st.session_state.historial) > 30:
        st.session_state.historial.pop(0)
    
    with placeholder.container():
        col1, col2 = st.columns(2)
        
        with col1:
            # Cálculo de la variación porcentual 📈
            if precio_anterior > 0:
                variacion_pct = ((nuevo_precio - precio_anterior) / precio_anterior) * 100
            else:
                variacion_pct = 0
            
            # Métrica con color automático (verde si sube, rojo si baja)
            st.metric(
                label="Bitcoin (USD) 🪙", 
                value=f"${nuevo_precio:,.2f}", 
                delta=f"{variacion_pct:.2f}%"
            )
        
        with col2:
            st.write("⏱️ **Última actualización**")
            st.info(time.strftime('%H:%M:%S'))
        
        st.divider()
        st.subheader("Evolución en tiempo real")
        st.line_chart(st.session_state.historial)
        
    time.sleep(15)
