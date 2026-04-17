# ... (dentro del bucle while True) ...
precio_actual = obtener_precio_crypto()

if precio_actual > 0:
    # Si tenemos un precio nuevo, lo añadimos
    st.session_state.historial.append(precio_actual)
else:
    # Si la API falló (precio 0.0), repetimos el último precio para que la gráfica no salte
    precio_actual = st.session_state.historial[-1]
    st.session_state.historial.append(precio_actual)
    st.info("Nota: Usando último precio conocido (esperando respuesta del mercado...)")
