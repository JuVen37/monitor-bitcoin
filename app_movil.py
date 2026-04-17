import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from gtts import gTTS
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="CREAL MULTI-USER AI", page_icon="🧬", layout="wide")

# Estilo Neón
st.markdown("<style>.main { background-color: #050505; color: #00ffc8; }</style>", unsafe_allow_html=True)

# --- SISTEMA MULTIUSUARIO (LOGIN) ---
with st.sidebar:
    st.title("👤 Acceso Usuario")
    nombre_usuario = st.text_input("Tu Nombre", value="Creal")
    user_id_telegram = st.text_input("Tu ID Telegram", value="8449303559")
    st.success(f"Conectado como: {nombre_usuario}")
    st.divider()
    st.info("Esta IA ahora es compartida. Cada usuario recibe sus propios avisos.")

# --- FUNCIONES DE VOZ Y TELEGRAM ---
def enviar_voz_telegram(texto):
    token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
    # Crear audio
    tts = gTTS(text=texto, lang='es')
    tts.save("respuesta.mp3")
    # Enviar a Telegram
    url = f"https://api.telegram.org/bot{token}/sendAudio?chat_id={user_id_telegram}"
    with open("respuesta.mp3", "rb") as audio:
        requests.post(url, files={'audio': audio})

# --- FUNCIÓN DE VISIÓN (SIMULADA PARA FACTURAS) ---
def analizar_factura(imagen):
    # Aquí es donde conectaríamos con Gemini Vision. 
    # Por ahora, simulamos el análisis experto:
    time.sleep(2)
    return f"Análisis para {nombre_usuario}: He detectado un precio de 0.21€/kWh. ¡Es un robo! El mercado real está a 0.12€. Te sugiero cambiar a una tarifa regulada."

# --- DASHBOARD DE DATOS ---
st.title(f"🧬 SISTEMA HOLÍSTICO - Hola {nombre_usuario}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("👁️ Visión: Analizar Factura")
    archivo = st.file_uploader("Sube foto de tu factura", type=['png', 'jpg', 'jpeg'])
    if archivo:
        with st.spinner("IA Analizando imagen..."):
            resultado = analizar_factura(archivo)
            st.warning(resultado)
            if st.button("Enviar veredicto a mi Telegram"):
                enviar_voz_telegram(resultado)

with col2:
    st.subheader("💬 Chat & Voz")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Hablemos..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        # Respuesta inteligente
        respuesta = f"Hola {nombre_usuario}, como tu IA personal, te digo que todo está bajo control. ¿Quieres que te mande la respuesta por audio?"
        if "luz" in p.lower(): respuesta = f"El precio actual es bajo. Es buen momento para gastar."
        
        with st.chat_message("assistant"):
            st.markdown(respuesta)
            if st.button("🔊 Escuchar respuesta en Telegram"):
                enviar_voz_telegram(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# --- REQUISITOS NUEVOS ---
# Importante: Añade 'gTTS' a tu archivo requirements.txt
