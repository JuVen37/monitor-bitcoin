import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. DISEÑO DE ÉLITE DEFINITIVA ---
st.set_page_config(page_title="CREAL OMNI: SINGULARITY", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: radial-gradient(circle at top, #0d1117 0%, #000000 100%); }
    .stChatMessage { border-radius: 20px; background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); }
    .stFileUploader section { background-color: #161b22 !important; border: 1px solid #4A90E2 !important; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# Recuperar Clave de Poder
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. PIEZA MAESTRA: MEMORIA DE SESIÓN ---
if "memoria" not in st.session_state:
    st.session_state.memoria = {"usuario": "Líder", "ultimo_analisis": None}

# --- 3. EL CEREBRO OMNIPOTENTE ---
def llamar_ia_omnipotente(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    
    instrucciones = f"""
    ERES CREAL OMNI SINGULARITY. Fecha: {fecha_hoy}.
    TU MISIÓN: Superar a ChatGPT en utilidad real y monetización.
    - SI HAY IMAGEN: Eres experto en Vinted. Da Título SEO, Descripción AIDA y Precio Realista. Cero rollos psicológicos.
    - SI PIDEN DISEÑO: Responde SOLO con un prompt detallado en inglés para generar una imagen.
    - SI ES TEXTO: Sé ejecutivo, breve y brillante.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "🌌 Conexión establecida. ¿Cuál es el objetivo?"

# --- 4. INTERFAZ DE CONTROL ---
st.markdown("<h1 style='text-align: center; color: white;'>♾️ OMNI SINGULARITY</h1>", unsafe_allow_html=True)

archivo = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
if archivo:
    if archivo.type.startswith("image"):
        st.image(archivo, width=250)
    st.session_state.memoria["ultimo_analisis"] = archivo.name

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar mensajes guardados
for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]:
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

# Entrada de comandos
if prompt := st.chat_input("Ejecutar comando..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        res = llamar_ia_omnipotente(prompt, img_data, m_type)

        # Si detectamos que la IA ha respondido con un prompt para imagen
        if any(x in res.lower() for x in ["design", "logo", "photorealistic"]) and len(res.split()) > 5:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Proyección Generada", use_container_width=True)
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Area para copiar texto fácil
            st.text_area("📋 Copiar resultado:", value=res, height=100)
            
            # Audio
            try:
                texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:250]
                tts = gTTS(text=texto_voz, lang='es')
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
            except:
                pass
