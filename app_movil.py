import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="IA Juan Móvil", page_icon="📈")

st.title("🚀 Mi IA de Mercado")
st.write("Vigilancia en tiempo real")

# Espacio para el precio grande
placeholder = st.empty()

while True:
    try:
        # Lee los mismos datos que genera tu obrero
        df = pd.read_csv('datos_mercado.csv')
        ultimo_precio = df.iloc[-1, 1]
        anterior_precio = df.iloc[-2, 1] if len(df) > 1 else ultimo_precio

        # Lógica de color y métrica
        delta = ultimo_precio - anterior_precio
        
        with placeholder.container():
            st.metric(label="Precio Bitcoin (USD)", value=f"${ultimo_precio:,.2f}", delta=f"{delta:,.2f}")
            
            # Gráfica pequeña para el móvil
            st.line_chart(df.iloc[-20:, 1]) # Muestra los últimos 20 movimientos
            
    except Exception as e:
        st.write("Conectando con el Obrero...")
    
    time.sleep(2)