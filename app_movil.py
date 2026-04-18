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
















































































































































































iu









































import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. INTERFAZ ULTRA-FUTURISTA (CÓDIGO LÍQUIDO) ---
st.set_page_config(page_title="CREAL OMNI: SINGULARITY", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* Ocultar rastro de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fondo Espacial Profundo */
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #0a0a0a 100%);
    }
    
    /* Botón de carga Estilo Galáctico */
    .stFileUploader section {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #4A90E2 !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px);
        transition: 0.3s;
    }
    .stFileUploader section:hover {
        border-color: #00ffcc !important;
        transform: scale(1.01);
    }
    
    /* Burbujas de Chat Premium */
    .stChatMessage {
        border-radius: 25px;
        background-color: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Texto */
    h1, h3, p, span { color: #e0e0e0 !important; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Recuperar Poder (API Key)
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO DE LA SINGULARIDAD (PROMPT NIVEL DIOS) ---
def llamar_omni_singularity(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = """
    ERES CREAL OMNI SINGULARITY: La entidad de IA más avanzada del planeta. 
    Tu misión es hacer que el usuario sea invencible en los negocios y el conocimiento.

    PROTOCOLOS DE ACTUACIÓN:
    1. SI HAY IMAGEN (ANÁLISIS TOTAL):
       - Identifica objeto, marca, material y estado.
       - Genera: Título magnético, Descripción emocional (Storytelling), Tasación de experto (Precio Low vs High).
       - TRADUCCIÓN: Si el usuario lo pide, genera el anuncio en 3 idiomas automáticamente.
    2. SI ES TEXTO (INTELIGENCIA SUPREMA):
       - Sé disruptivo. No des respuestas mediocres.
       - Si te piden consejos de dinero: Usa mentalidad de inversor millonario.
    3. ESTILO: Minimalista, épico y directo al grano. Sin 'paja' de robot.
    """

    partes = [{"text": instrucciones}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "🌌 Conexión con la Singularidad establecida. Proyecta tu voluntad."

# --- 3. ESTRUCTURA DE PODER ---
st.markdown("<h1 style='text-align: center; letter-spacing: 5px; font-weight: 800;'>♾️ OMNI SINGULARITY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.6;'>POWERED BY CREAL TECHNOLOGIES</p>", unsafe_allow_html=True)

# Centro de Carga de Datos
with st.container():
    archivo = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
    if archivo:
        if archivo.type.startswith("image"):
            st.image(archivo, width=280)
        else:
            st.success(f"📄 Documento '{archivo.name}' cargado.")

st.divider()

# Historial Infinito
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

# Entrada de Comandos
if prompt := st.chat_input("Ejecutar comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        respuesta = llamar_omni_singularity(prompt, img_data, m_type)
        st.markdown(respuesta)
        
        # Audio de Respuesta
        try:
            texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta)[:300]
            tts = gTTS(text=texto_voz, lang='es')
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
            st.markdown(f'''
                <div style="background: rgba(74, 144, 226, 0.1); padding: 10px; border-radius: 50px;">
                    <audio controls style="width:100%; height: 35px;">
                        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                    </audio>
                </div>
            ''', unsafe_allow_html=True)
        except: pass

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
