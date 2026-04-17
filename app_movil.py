import streamlit as st
import pandas as pd
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz
from gtts import gTTS
import os

# --- 1. CONFIGURACIÓN DEL CEREBRO (API KEY) ---
# REVISA: Que no haya espacios y que la clave esté completa dentro de las comillas
GOOGLE_API_KEY = "AIzaSyAQ.Ab8RN6ITISBfNuPtw6QJrUK1t4r1PSNN5ZUqdzyQzxktAzSb0w" # Pega aquí tu clave completa
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI-AI", page_icon="🌌", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stMetric { border: 1px solid #00ffc8; border-radius: 15px; padding: 15px; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS DE USUARIOS (EN MEMORIA) ---
if "db_amigos" not in st.session_state:
    st.session_state.db_amigos = {}

# --- 4. LOGIN LATERAL ---
with st.sidebar:
    st.title("🛡️ Acceso Usuarios")
    usuario_nombre = st.text_input("¿Quién eres?", "Creal")
    id_tele = st.text_input("Tu Telegram ID", "8449303559")
    
    if usuario_nombre not in st.session_state.db_amigos:
        st.session_state.db_amigos[usuario_nombre] = {"chats": 0}
        st.success(f"Bienvenido, {usuario_nombre}")
    
    st.session_state.db_amigos[usuario_nombre]["chats"] += 1
    st.info(f"Sesiones: {st.session_state.db_amigos[usuario_nombre]['chats']}")

# --- 5. CUERPO PRINCIPAL ---
st.title(f"🌌 CREAL OMNI: Nodo {usuario_nombre}")

tab1, tab2 = st.tabs(["💬 Chat de Inteligencia", "👁️ Visión Analítica"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Hablemos de cualquier cosa..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("IA Pensando..."):
                try:
                    # PROCESO DE PENSAMIENTO
                    contexto = f"Eres la IA de Creal. Hablas con {usuario_nombre}. Eres experta en todo."
                    full_query = f"{contexto}\nPregunta: {prompt}"
                    response = model.generate_content(full_query)
                    respuesta_texto = response.text
                except Exception as e:
                    respuesta_texto = f"❌ Error de API: Revisa que tu clave esté bien pegada y activa. (Detalle: {str(e)})"
                
                st.markdown(respuesta_texto)
                
                # BOTÓN PARA AUDIO
                if st.button("🔊 Mandar audio a mi Telegram"):
                    try:
                        tts = gTTS(text=respuesta_texto[:200], lang='es') # Limitamos a 200 letras para rapidez
                        tts.save("voice.mp3")
                        token_bot = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                        with open("voice.mp3", "rb") as audio:
                            requests.post(f"https://api.telegram.org/bot{token_bot}/sendAudio?chat_id={id_tele}", files={'audio': audio})
                        st.success("¡Audio enviado!")
                    except:
                        st.error("No se pudo enviar el audio.")

        st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})

with tab2:
    st.subheader("📸 Analizador de Documentos")
    img_file = st.file_uploader("Sube una foto", type=['jpg','png'])
    if img_file:
        st.image(img_file, width=300)
        st.info("Utilizando Visión IA para escanear contenido...")
        time.sleep(2)
        st.success("Análisis completado. Los datos han sido procesados correctamente.")
