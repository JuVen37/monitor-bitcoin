import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. DISEÑO PROFESIONAL (INTERFAZ LIMPIA) ---
st.set_page_config(page_title="CREAL OMNI BUSINESS", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0b0d11; }
    
    .stFileUploader section {
        background-color: #1e1f22 !important;
        border: 2px dashed #4A90E2 !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }
    
    .stChatMessage {
        border-radius: 20px;
        background-color: #1e1f22;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO DE VENTAS DIRECTAS (SIN PSICOLOGÍA) ---
def llamar_ia_vendedor(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = """
    Eres CREAL OMNI BUSINESS, el mejor experto en ventas de Vinted y Wallapop.
    
    REGLA DE ORO: No uses rollos de psicología, ni hables de "sentimientos" o "autoestima". 
    Céntrate en DATOS REALES DE VENTA.
    
    SI HAY IMAGEN:
    1. Identifica: Marca, Talla (si se ve), Color y Estilo.
    2. TÍTULO: Directo y con palabras clave (SEO).
    3. DESCRIPCIÓN: Describe la prenda físicamente. Di si está como nueva, si es tendencia y cómo combinarla. Sé persuasivo pero REALISTA.
    4. PRECIO: Da un precio para vender hoy mismo y otro para ganar lo máximo.
    5. HASHTAGS: Los 5 que más visitas traen.

    SI ES TEXTO: Sé ejecutivo, breve y ayuda al usuario a ganar dinero.
    """

    partes = [{"text": instrucciones}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión lista. ¿Qué vamos a vender?"

# --- 3. ESTRUCTURA ---
st.markdown("<h2 style='text-align: center; color: white;'>⚡ CREAL OMNI BUSINESS</h2>", unsafe_allow_html=True)

foto = st.file_uploader("➕ SUBIR FOTO PARA VENDER", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, width=200)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "⚡" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

if prompt := st.chat_input("Escribe detalles de la prenda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        respuesta = llamar_ia_vendedor(prompt, img_data, m_type)
        st.markdown(respuesta)
        
        try:
            texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta)[:300]
            tts = gTTS(text=texto_voz, lang='es')
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
            st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
        except: pass

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
