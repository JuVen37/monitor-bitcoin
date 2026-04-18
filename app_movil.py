import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. ESTÉTICA DE LUJO (DARK PREMIUM) ---
st.set_page_config(page_title="CREAL OMNI BUSINESS", page_icon="💰", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    .stChatMessage {border-radius: 20px; border: 1px solid #1f2937;}
    /* Botón de carga personalizado */
    .stFileUploader {border: 2px dashed #4A90E2; border-radius: 15px; padding: 10px;}
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()
if not API_KEY:
    st.error("🔑 Configura la API KEY.")
    st.stop()

# --- 2. EL CEREBRO MILLONARIO ---
def llamar_ia_business(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    # Este 'prompt' está diseñado para superar a cualquier IA comercial
    instrucciones_maestras = """
    Eres CREAL OMNI BUSINESS, la IA más potente para generar beneficios. 
    Tu objetivo es que el usuario GANE DINERO.
    
    SI RECIBES UNA FOTO DE ROPA/OBJETO:
    - No seas un robot. Sé un experto en marketing de lujo.
    - TÍTULO: Debe ser irresistible y SEO optimizado.
    - DESCRIPCIÓN: Usa la técnica AIDA (Atención, Interés, Deseo, Acción). Resalta por qué esta prenda es única.
    - TASACIÓN PRO: Analiza la marca y el estado. Da un precio de 'Venta Rápida' y un precio de 'Máximo Beneficio'.
    - CONSEJO DE ORO: Da un truco extra (ej: 'Haz la foto con luz natural para venderla un 20% más cara').
    
    SI ES TEXTO GENERAL:
    - Sé brillante, breve y ofrece ideas para monetizar o mejorar la productividad.
    """

    partes = [{"text": instrucciones_maestras}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "💰 Sistemas listos. Vamos a generar valor."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: white;'>⚡ CREAL OMNI <span style='color:#4A90E2;'>BUSINESS</span></h1>", unsafe_allow_html=True)

with st.container():
    foto = st.file_uploader("📸 ESCANEAR PARA MONETIZAR", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, width=300)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemas listos para el negocio. ¿Qué vamos a vender hoy?"}]

for m in st.session_state.messages:
    avatar = "⚡" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

if prompt := st.chat_input("Escribe tu consulta o detalle de producto..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        respuesta = llamar_ia_business(prompt, img_data, m_type)
        st.markdown(respuesta)
        
        # Audio de alta fidelidad
        try:
            texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta)[:250]
            tts = gTTS(text=texto_voz, lang='es')
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
            st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
        except: pass

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
