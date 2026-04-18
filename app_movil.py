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
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajuste para que el botón de subir foto no ocupe toda la pantalla */
    .stFileUploader {
        padding-top: 0px;
        margin-bottom: -20px;
    }
    
    /* Estilo para los mensajes */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()
if not API_KEY:
    st.error("🔑 Error: Configura la API KEY en Secrets.")
    st.stop()

# --- 2. MOTOR DE IA AVANZADO ---
def llamar_ia_pro(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones_maestras = """
    Eres CREAL OMNI, una IA de élite para ventas en Vinted.
    Si recibes una imagen: Analízala como un experto en moda. 
    1. Crea un Título optimizado.
    2. Crea una descripción que venda (menciona estado, estilo y tips).
    3. Pon un PRECIO estimado realista para ganar dinero.
    4. Añade hashtags.
    Si no hay imagen: Sé el mejor asistente personal del mundo.
    """

    partes = [{"text": instrucciones_maestras}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "🤯 He tenido un pequeño chispazo cerebral. ¿Puedes repetir eso?"

# --- 3. INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>⚡ CREAL OMNI <span style='color:#4A90E2;'>PRO</span></h1>", unsafe_allow_html=True)

# --- BOTÓN DE SUBIR FOTO (AHORA EN EL CENTRO) ---
# Lo ponemos dentro de una pequeña caja para que se vea bien en el móvil
with st.container():
    foto = st.file_uploader("📸 TOCA AQUÍ PARA SUBIR TU PRENDA", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, caption="Foto lista para analizar", width=200)

st.divider()

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Sube la foto de lo que quieras vender arriba y dime la marca. ¡Vamos a por ese dinero! 💸"}]

for m in st.session_state.messages:
    avatar_icon = "⚡" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar_icon):
        st.markdown(m["content"])

# Entrada de chat (está al lado del botón de enviar por defecto en Streamlit)
if prompt := st.chat_input("Escribe detalles (marca, talla...)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        respuesta = llamar_ia_pro(prompt, img_data, m_type)
        st.markdown(respuesta)
        
        # Audio
        try:
            texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta)[:250]
            tts = gTTS(text=texto_voz, lang='es')
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
            st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
        except: pass

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
