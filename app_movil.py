import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse

# --- 1. CONFIGURACIÓN Y BORRADO ATÓMICO (SIN RASTROS) ---
st.set_page_config(page_title="OMNI-X", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* 1. ELIMINAR TODA LA BARRA SUPERIOR Y ELEMENTOS DE ESTADO */
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    
    /* 2. ELIMINAR LOS ICONOS DE ABAJO (COMUNIDAD Y CORONA) */
    .stAppToolbar {display: none !important;}
    footer {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* 3. QUITAR LÍNEAS Y MARGENES EXTRA */
    .stDeployButton {display:none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* 4. AJUSTE DE PANTALLA TOTAL */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -50px !important; /* Sube todo para tapar la línea blanca */
    }

    /* 5. FONDO NEGRO PURO */
    .stApp {
        background: #000000 !important;
        color: #ffffff;
    }
    
    /* Ocultar el botón de 'Stop' que sale arriba a veces */
    button[title="Stop running"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. MOTOR OMNI-X ---
def llamar_ia_omni(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    instrucciones = "Eres OMNI-X. Resuelve todo de forma brillante y directa."

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Sistemas listos."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2; font-size: 38px;'>♾️ OMNI-X</h1>", unsafe_allow_html=True)

foto = st.file_uploader("", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, width=250)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]: st.image(m["content"])
        else: st.markdown(m["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        res = llamar_ia_omni(prompt, img_data, m_type)

        if any(x in res.lower() for x in ["crea", "logo", "imagen"]) and len(res.split()) > 4:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img)
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Bot
