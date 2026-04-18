import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse

# --- 1. PROTOCOLO DE OCULTACIÓN TOTAL (MOVIL OPTIMIZED) ---
st.set_page_config(page_title="OMNI-X", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* 1. OCULTAR BARRA SUPERIOR Y LÍNEA DE CARGA */
    header, [data-testid="stHeader"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 2. OCULTAR ICONOS DE ABAJO (CORONA, COMUNIDAD, ETC.) */
    [data-testid="stToolbar"], .stAppToolbar, [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 3. ELIMINAR CUALQUIER ELEMENTO FLOTANTE DE STREAMLIT */
    #MainMenu, footer, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* 4. FORZAR FONDO NEGRO PURO EN TODA LA APP */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* 5. AJUSTAR CONTENEDOR PARA ELIMINAR ESPACIOS BLANCOS */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -40px !important;
    }

    /* 6. OCULTAR EL BOTÓN DE CARGA/ESTADO QUE SALE EN MÓVILES */
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* 7. ESTILO DE CHAT LIMPIO */
    .stChatMessage {
        background-color: #111111 !important;
        border: 1px solid #222222 !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. MOTOR OMNI-X ---
def motor_omni_x(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    instrucciones = "Eres OMNI-X. Resuelve con brillantez."

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión segura."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2; font-size: 32px;'>♾️ OMNI-X</h1>", unsafe_allow_html=True)

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

if prompt := st.chat_input("Comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        res = motor_omni_x(prompt, img_data, m_type)

        if any(x in res.lower() for x in ["crea", "logo", "imagen"]) and len(res.split()) > 4:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img)
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Herramientas
            col1, col2 = st.columns(2)
            col1.link_button("📱 WhatsApp", f"https://wa.me/?text={urllib.parse.quote(res)}")
            col2.button("🔄 Borrar", on_click=lambda: st.session_state.clear())
            
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:200]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
