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
    
    /* Estilo de los mensajes */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
    }
    
    /* Personalización del fondo y fuentes */
    stApp {
        background-color: #0d1117;
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
    
    # INSTRUCCIONES MAESTRAS (Aquí es donde superamos a ChatGPT)
    instrucciones_maestras = """
    Eres CREAL OMNI, una IA de élite superior en precisión y utilidad. 
    Tu objetivo es ser más directo, creativo y útil que cualquier otra IA.
    
    REGLAS DE ORO:
    1. Si te pasan una foto de ropa para Vinted: Sé un tiburón de las ventas. Da el mejor título, 
       descripción emocional y tasa el precio basándote en tendencias actuales de mercado.
    2. Si es una consulta general: Sé brillante, breve y evita las frases típicas de robot.
    3. Usa siempre emojis que encajen con el tono.
    4. Si detectas fallos en la foto (arrugas, mala luz), dáselo como consejo al usuario para mejorar su venta.
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

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center;'>⚡ CREAL OMNI <span style='color:#4A90E2;'>PRO</span></h1>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.title("Panel de Control")
    user_name = st.text_input("Piloto:", "Juan")
    st.divider()
    foto = st.file_uploader("📸 Analizador de Visión (Vinted/Objetos)", type=["jpg", "png", "jpeg"])
    if foto: st.image(foto, use_container_width=True)

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Sistemas listos. ¿Qué misión tenemos hoy, **{user_name}**?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="⚡" if m["role"] == "assistant" else "👤"):
        st.markdown(m["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu comando..."):
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
