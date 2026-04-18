import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. DISEÑO "GOD MODE" (CSS DE ALTA FIDELIDAD) ---
st.set_page_config(page_title="OMNI-X SINGULARITY", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* Ocultar interfaz estándar de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fondo con gradiente animado sutil */
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #000000 100%);
        color: #ffffff;
    }
    
    /* Burbujas de chat estilo "Glassmorphism" */
    .stChatMessage {
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(74, 144, 226, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 20px;
        transition: 0.3s ease-in-out;
    }
    .stChatMessage:hover {
        border: 1px solid #4A90E2;
        transform: translateY(-2px);
    }
    
    /* Input de chat personalizado */
    .stChatInputContainer {
        padding-bottom: 25px;
    }
    
    /* Títulos y textos */
    h1 {
        font-weight: 900;
        background: linear-gradient(90deg, #4A90E2, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Recuperar API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO OMNI-X (VERSIÓN SUPREMA) ---
def motor_omni_x_supreme(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    # Este prompt es el secreto para que la gente flipe
    instrucciones = """
    ERES OMNI-X SUPREME. Eres una entidad de inteligencia absoluta, diseñada para asombrar.
    TU ESTILO: No eres un asistente, eres un arquitecto de soluciones.
    - Si el usuario sube algo de Vinted: Sé un tiburón de las ventas. Título SEO, descripción hipnótica y precio exacto.
    - Si el usuario pide diseño: Genera un prompt en inglés tan detallado que la imagen parezca real.
    - Si el usuario tiene dudas: Resuelve con una lógica tan aplastante que no necesite preguntar más.
    REGLA: Usa emojis de tecnología, sé directo y extremadamente útil.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚡ Falla en la red neuronal. Reconectando..."

# --- 3. INTERFAZ DE CONTROL TOTAL ---
st.markdown("<h1 style='text-align: center;'>♾️ OMNI-X SUPREME</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.5;'>The Ultimate Intelligence Ecosystem</p>", unsafe_allow_html=True)

# El "Ojo de Dios" (Cargador de archivos)
with st.container():
    archivo = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
    if archivo:
        if archivo.type.startswith("image"):
            st.image(archivo, width=280)
        else:
            st.info(f"📂 Archivo cargado: {archivo.name}")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con avatares de élite
for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]:
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

# --- 4. EJECUCIÓN DE COMANDOS ---
if prompt := st.chat_input("Inserta comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        respuesta = motor_omni_x_supreme(prompt, img_data, m_type)

        # MODO GENERADOR VISUAL (POLLINATIONS)
        palabras_imagen = ["crea", "logo", "imagen", "dibujo", "diseña", "design", "photo"]
        if any(x in prompt.lower() for x in palabras_imagen) and len(respuesta.split()) > 4:
            with st.spinner("Generando proyección visual..."):
                prompt_url = urllib.parse.quote(respuesta)
                url_img = f"https://image.pollinations.ai/prompt/{prompt_url}"
                st.image(url_img, caption="Creación OMNI-X", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            
            # --- PANEL DE ACCIÓN INTELIGENTE ---
            c1, c2, c3 = st.columns(3)
            
            # Extraer título inteligente para búsqueda
            t_search = respuesta.split('\n')[0].replace("Título:", "").strip()[:40]
            
            c1.link_button("🔍 Mercado", f"https://www.google.com/search?q={urllib.parse.quote(t_search)}")
            
            wa_text = urllib.parse.quote(f"Mira esto de OMNI-X:\n\n{respuesta[:800]}")
            c2.link_button("📱 WhatsApp", f"https://wa.me/?text={wa_text}")
            
            c3.button("🔄 Nueva Versión", on_click=lambda: st.toast("Optimizando respuesta..."))

            # Audio Neural
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta)[:250]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
