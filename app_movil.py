import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse

# --- 1. CONFIGURACIÓN Y ELIMINACIÓN DE MARCAS ---
st.set_page_config(page_title="OMNI-X", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* 1. OCULTAR TODO EL HEADER Y FOOTER (Adiós a 'Created by') */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    
    /* 2. ELIMINAR ESPACIO EN BLANCO SUPERIOR */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }

    /* 3. ESTÉTICA GHOST DARK */
    .stApp {
        background: radial-gradient(circle at center, #101218 0%, #000000 100%);
        color: #ffffff;
    }
    
    /* 4. BURBUJAS DE CHAT */
    .stChatMessage {
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(74, 144, 226, 0.15);
        margin-bottom: 12px;
    }
    
    /* 5. OCULTAR MARCA DE AGUA DEL INPUT */
    footer:after {
        content:''; 
        display:none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key (Invisible)
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. MOTOR OMNI-X ---
def llamar_ia_omni(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    instrucciones = "Eres OMNI-X, una inteligencia superior. No te presentes. Resuelve retos, analiza fotos y maximiza el valor para el usuario."

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Sistemas activos. ¿Cuál es el comando?"

# --- 3. INTERFAZ LIMPIA Y EXCLUSIVA ---
st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #4A90E2, #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 40px;'>♾️ OMNI-X</h1>", unsafe_allow_html=True)

# Subida de archivos integrada
foto = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
if foto:
    if foto.type.startswith("image"):
        st.image(foto, width=280)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial de Chat
for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]:
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

# Entrada de usuario
if prompt := st.chat_input("Inserta comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if foto and foto.type.startswith("image"):
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        res = llamar_ia_omni(prompt, img_data, m_type)

        # Generador de Imagen Inteligente
        if any(x in prompt.lower() for x in ["crea", "logo", "imagen", "diseña"]) and len(res.split()) > 4:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Creación Finalizada", use_container_width=True)
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Herramientas de Acción
            col1, col2 = st.columns(2)
            wa_text = urllib.parse.quote(f"Respuesta de OMNI-X:\n\n{res}")
            col1.link_button("📱 WhatsApp", f"https://wa.me/?text={wa_text}")
            col2.button("🔄 Nueva Sesión", on_click=lambda: st.session_state.clear())
            
            # Audio Neural
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:250]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
