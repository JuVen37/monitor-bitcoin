import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. INTERFAZ DE ÉLITE DEFINITIVA ---
st.set_page_config(page_title="CREAL OMNI: SINGULARITY", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: radial-gradient(circle at top, #0d1117 0%, #000000 100%); }
    .stChatMessage { border-radius: 20px; background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); }
    .stFileUploader section { background-color: #161b22 !important; border: 1px solid #4A90E2 !important; border-radius: 15px; }
    /* Botones de acción rápida */
    .stButton>button { width: 100%; border-radius: 20px; background-color: #238636; color: white; border: none; }
    </style>
""", unsafe_allow_html=True)

# Recuperar Clave de Poder
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. PIEZA MAESTRA: MEMORIA DE LARGO PLAZO ---
if "memoria" not in st.session_state:
    st.session_state.memoria = {
        "usuario": "Líder",
        "ultimo_analisis": None,
        "objetivos": "Ganar dinero y eficiencia"
    }

# --- 3. EL CEREBRO OMNIPOTENTE (CON NAVEGACIÓN Y ACCIÓN) ---
def llamar_ia_omnipotente(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    
    instrucciones = f"""
    ERES CREAL OMNI SINGULARITY (VERSIÓN OMNIPOTENTE). Fecha actual: {fecha_hoy}.
    TU MISIÓN: Superar a ChatGPT en utilidad real y monetización.

    PROTOCOLOS ACTIVADOS:
    1. MEMORIA: Recuerda que el usuario busca maximizar beneficios. Contexto previo: {st.session_state.memoria}.
    2. NAVEGACIÓN (Simulada): Actúa como si estuvieras conectado a la red. Si te piden precios, estima basándote en la inflación y tendencias de 2024-2025.
    3. ACCIÓN VINTED: Si ves ropa, genera:
       - Título Ganador.
       - Descripción 'Copywriting Pro' (Atención, Deseo, Acción).
       - Tasación de Mercado Realista.
    4. DISEÑO: Si piden logos, genera un prompt en inglés para DALL-E/Pollinations.
    5. CERO RELLENO: No digas "Hola", no digas "Sistemas listos". Ve directo al resultado.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "🌌 Singularidad lista. Proyecta tu voluntad."

# --- 4. INTERFAZ DE CONTROL ---
st.markdown("<h1 style='text-align: center; color: white; font-weight: 900;'>♾️ OMNI SINGULARITY</h1>", unsafe_allow_html=True)

# Slot de entrada de archivos (Visión/Docs)
archivo = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
if archivo:
    if archivo.type.startswith("image"):
        st.image(archivo, width=280)
    st.session_state.memoria["ultimo_analisis"] = archivo.name

st.divider()

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]:
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

# Entrada de comandos
if prompt := st.chat_input("Ejecutar comando maestro..."):
    st.session_state.messages.append({"role":
