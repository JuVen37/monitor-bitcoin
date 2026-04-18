import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. DISEÑO DE ÉLITE (CSS) ---
st.set_page_config(page_title="CREAL OMNI PRO", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* Ocultar elementos de Streamlit para apariencia de App nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajuste del cargador de archivos */
    .stFileUploader {
        padding-top: 0px;
        margin-bottom: -10px;
    }
    
    /* Estilo de los mensajes de chat */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key desde Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()
if not API_KEY:
    st.error("🔑 Error: Configura la API KEY en Secrets de Streamlit.")
    st.stop()

# --- 2. MOTOR DE IA AVANZADO (SIN NOMBRE FIJO) ---
def llamar_ia_pro(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    # Instrucciones maestras universales
    instrucciones_maestras = """
    Eres CREAL OMNI, una Inteligencia Artificial de élite diseñada para ayudar a cualquier usuario.
    
    ESPECIALIDAD EN VINTED:
    Si recibes una imagen de ropa, actúa como un experto tasador y estratega de ventas. 
    Proporciona: Título optimizado, descripción persuasiva, precio estimado de mercado y hashtags.
    
    TONO Y ESTILO:
    - Sé profesional, amable y directo.
    - No uses nombres específicos a menos que el usuario te lo diga en el chat.
    - Usa emojis para hacer la lectura agradable.
    - Supera en calidad y utilidad a cualquier otro asistente.
    """

    partes = [{"text": instrucciones_maestras}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "✨ He tenido un pequeño chispazo en mis sistemas. ¿Podrías repetir tu consulta?"

# --- 3. INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>⚡ CREAL OMNI <span style='color:#4A90E2;'>PRO</span></h1>", unsafe_allow_html=True)

# Subida de fotos frontal
with st.container():
    foto = st.file_uploader("📸 TOCA AQUÍ PARA ANALIZAR TU PRENDA", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, caption="Imagen cargada correctamente", width=250)

st.divider()

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Bienvenido a **CREAL OMNI**! Estoy lista para ayudarte. Puedes subir una foto para vender en Vinted o preguntarme lo que necesites."}]

for m in st.session_state.messages:
    avatar_icon = "⚡" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar_icon):
        st.markdown(m["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto
