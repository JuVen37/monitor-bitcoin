import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. DISEÑO "GHOST MODE" (OCULTA TODO RASTRO DE CUENTA) ---
st.set_page_config(page_title="OMNI-X", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* OCULTAR BARRA SUPERIOR, LOGO DE STREAMLIT Y MENÚ DE CUENTA */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stStatusWidget"] {display:none !important;}
    
    /* Fondo y estética profesional */
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #000000 100%);
        color: #ffffff;
    }
    
    /* Burbujas de chat */
    .stChatMessage {
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(74, 144, 226, 0.2);
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key desde secrets (Invisible para el usuario)
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO OMNI-X ---
def motor_omni_x(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    instrucciones = "Eres OMNI-X, una IA de élite. Resuelve cualquier duda, analiza imágenes y ayuda al usuario a ganar dinero o tiempo."

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚡ Sistema en línea."

# --- 3. INTERFAZ LIMPIA ---
st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #4A90E2, #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>♾️ OMNI-X</h1>", unsafe_allow_html=True)

# Cargador
archivo = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
if archivo:
    if archivo.type.startswith("image"):
        st.image(archivo, width=280)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial
for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]:
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

# Entrada de chat
if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        res = motor_omni_x(prompt, img_data, m_type)

        # Generador de Imagen
        if any(x in prompt.lower() for x in ["crea", "logo", "imagen"]) and len(res.split()) > 4:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Generado", use_container_width=True)
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Herramientas
            col1, col2 = st.columns(2)
            wa_text = urllib.parse.quote(f"OMNI-X dice:\n\n{res}")
            col1.link_button("📱 WhatsApp", f"https://wa.me/?text={wa_text}")
            col2.button("🔄 Reiniciar", on_click=lambda: st.session_state.clear())
            
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:200]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
