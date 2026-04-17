import streamlit as st
import pandas as pd
import time
import requests

# Configuración de la página
st.set_page_config(page_title="IA Juan Móvil", page_icon="📈")

st.title("🚀 Mi IA de Mercado")
st.write("Vigilancia 24/7 desde la nube (vía CoinGecko)")

# Nueva función para obtener el precio sin bloqueos geográficos
def obtener_precio_crypto():
    # Usamos CoinGecko en lugar de Binance para evitar bloqueos en la nube
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        # CoinGecko devuelve los datos así: {'bitcoin': {'usd': 65000}}
        return float(datos['bitcoin']['usd'])
    except Exception as e:
        st.error(f"Error al conectar con el mercado: {e}")
        return 0.0

# Inicializamos el historial en la memoria de la web
if 'historial' not in st.session_state:
    primer_precio = obtener_precio_crypto()
    st.session_state.historial = [primer_precio]

# Contenedor para que la web se actualice sin recargar toda la página
placeholder = st.empty()

# Bucle infinito de vigilancia
while True:
    precio_actual = obtener_precio_crypto()
    
    if precio_actual > 0:
        precio_anterior = st.session_state.historial[-1]
        st.session_state.historial.append(precio_actual)
        
        # Guardamos solo los últimos 30 puntos para que la gráfica se vea bien
        if len(st.session_state.historial) > 30:
            st.session_state.historial.pop(0)

        delta = precio_actual - precio_anterior
        
        with placeholder.container():
            # Mostramos el precio con estilo de bolsa
            st.metric(
                label="Bitcoin (BTC/USD)", 
                value=f"${precio_actual:,.2f}", 
                delta=f"${delta:,.2f}"
            )
            # Dibujamos la gráfica
            st.line_chart(st.session_state.historial)
    
    # Esperamos 10 segundos (CoinGecko es un poco más lento que Binance)
    time.sleep(10)
