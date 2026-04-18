import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. DISEÑO DE INTERFAZ MINIMALISTA (ESTILO APPLE/OPENAI) ---
st.set_page_config(page_title="CREAL OMNI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo y tipografía */
    .stApp {background-color: #0b0d11;}
    
    /* Estilo del botón "+" de subida */
    .stFileUploader section {
        background-color: #1e1f22 !important;
        border: 1px dashed #4A90E2 !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 10px !important;
    }
    
    /* Burbujas de chat */
    .stChatMessage {
        border-radius: 20px;
        background-color: #1e1f22;
        margin-bottom: 10px;
        padding: 15px;
    }
    
    /* Ajuste para móviles */
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO DE LA IA ---
def llamar_ia_master(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = """
    Eres CREAL OMNI BUSINESS. Tu única misión es ser la IA más útil del planeta.
    - Si recibes imagen: Eres el mejor experto en Vinted y ventas online. Analiza, tasa y redacta anuncios de éxito.
    - Si recibes texto: Sé ejecutivo, resolutivo y brillante.
    - Responde siempre con audacia. Sin introducciones innecesarias.
    """

    partes = [{"text": instrucciones}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión activa. ¿Cuál es el objetivo?"

# --- 3. ESTRUCTURA DE LA APP ---
st.markdown("<h3 style='text-align: center; color: white; opacity: 0.8;'>⚡ CREAL OMNI</h3>", unsafe_allow_html=True)

# EL BOTÓN "+" VISIBLE ARRIBA (Para que nadie se pierda)
foto = st.file_uploader("➕ AÑADIR ARCHIVO O FOTO", type=["jpg", "png", "jpeg", "pdf"])
if foto:
    st.image(foto, width=150, caption="Documento/Imagen listo")

st.divider()

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar chat
for m in st.session_state.messages:
    avatar = "⚡" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# Barra de chat
if prompt := st.chat_input("Escribe un comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        respuesta = llamar_ia_master(prompt, img_data, m_type)
        st.markdown(respuesta)
        
        # Audio Pro
        try:
            texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta)[:250]
            tts = gTTS(text=texto_voz, lang='es')
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
            st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
        except: pass

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
