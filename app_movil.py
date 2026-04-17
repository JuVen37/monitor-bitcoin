import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="IA Juan Móvil", page_icon="📈")

st.title("🚀 Mi IA de Mercado")
st.write("Vigilancia 24/7 desde la nube")

# Función que hace el trabajo del "Obrero"
def obtener_precio_crypto():
    url = "https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        
        # Verificamos si 'price' está en los datos antes de usarlo
        if 'price' in datos:
            return float(datos['price'])
        else:
            st.error(f"Binance respondió algo inesperado: {datos}")
            return 0.0
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return 0.0

# Inicializamos una lista en la memoria de la web para guardar los precios
if 'historial' not in st.session_state:
    st.session_state.historial = [obtener_precio_crypto()]

placeholder = st.empty()

while True:
    try:
        precio_actual = obtener_precio_crypto()
        precio_anterior = st.session_state.historial[-1]
        
        # Guardamos el nuevo precio en el historial
        st.session_state.historial.append(precio_actual)
        
        # Solo mantenemos los últimos 20 para la gráfica
        if len(st.session_state.historial) > 20:
            st.session_state.historial.pop(0)

        delta = precio_actual - precio_anterior
        
        with placeholder.container():
            st.metric(label="Bitcoin (BTC/USDT)", value=f"${precio_actual:,.2f}", delta=f"{delta:,.2f}")
            st.line_chart(st.session_state.historial)
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    
    time.sleep(5) # Espera 5 segundos para la siguiente actualización
