import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. DISEÑO DE ÉLITE (CHATGPT UI CLONE) ---
st.set_page_config(page_title="CREAL OMNI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* Ocultar basura de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo ultra oscuro profesional */
    .stApp {background-color: #0b0d11;}
    
    /* Estilo de los mensajes */
    .stChatMessage {
        border-radius: 20px;
        border: none;
        background-color: #1e1f22;
        margin-bottom: 15px;
        padding: 15px;
    }
    
    /* Contenedor del chat para que no choque con el input */
    .main .block-container {
        padding-bottom: 150px;
    }

    /* Estilo del botón de carga para que parezca el '+' de ChatGPT */
    .stFileUploader section {
        background-color: #2b2d31 !important;
        border: 1px solid #4A90E2 !important;
        border-radius: 10px !important;
        padding: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. MOTOR DE IA BUSINESS ---
def llamar_ia_master(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = """
    Eres CREAL OMNI BUSINESS, la IA más avanzada del mercado. Tu objetivo es generar riqueza y soluciones de élite.
    - Si hay imagen: Eres experto en Vinted/E-commerce. Crea títulos magnéticos, descripciones AIDA, precios de beneficio máximo y hashtags.
    - Si es texto: Sé brillante, ejecutivo y extremadamente útil.
    - No te presentes. No digas 'Sistemas listos'. Solo responde con poder.
    """

    partes = [{"text": instrucciones}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión establecida. Dime tu objetivo."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>⚡ CREAL OMNI</h1>", unsafe_allow_html=True)

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar mensajes
for m in st.session_state.messages:
    avatar = "⚡" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# --- 4. ZONA DE ENTRADA (ESTILO CHATGPT) ---
# Ponemos el cargador de archivos justo antes del chat input de forma discreta
with st.sidebar:
    st.markdown("### 🛠️ Herramientas")
    foto = st.file_uploader("➕ Añadir imagen (Vinted/Visión)", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, caption="Imagen cargada", use_container_width=True)
    st.divider()
    st.caption("Versión Business 2.5")

# Barra de chat
if prompt := st.chat_input("Escribe un mensaje..."):
    # Añadir mensaje de usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Respuesta IA
    with st.chat_message("assistant", avatar="⚡"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        respuesta = llamar_ia_master(prompt, img_data, m_type)
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
