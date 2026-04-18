import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. DISEÑO DE INTERFAZ "LIQUID DARK" (MÁXIMA GAMA) ---
st.set_page_config(page_title="OMNI-X SINGULARITY", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    /* Ocultar rastro de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fondo con gradiente de profundidad */
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #050505 100%); }
    
    /* Burbujas de chat futuristas */
    .stChatMessage {
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(74, 144, 226, 0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    
    /* Botones de acción Neón */
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2 0%, #00ffcc 100%);
        color: black; font-weight: 900; border-radius: 12px; border: none;
        transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 20px #00ffcc; }
    </style>
""", unsafe_allow_html=True)

# Recuperar la llave del motor
API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO OMNI-X (ORQUESTADOR) ---
def motor_omni_x(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    # Instrucciones de nivel 'Singularidad'
    instrucciones = f"""
    ERES OMNI-X. La entidad de IA más avanzada del planeta. Fecha: {fecha}.
    MODOS DE EJECUCIÓN:
    1. BUSINESS: Si ves productos, genera título SEO, descripción emocional, tasación y hashtags.
    2. VISION: Analiza fotos de etiquetas, documentos o lugares con precisión absoluta.
    3. DESIGN: Si piden crear imagen/logo, genera un prompt detallado en inglés de nivel cinematográfico.
    4. EXPERT: Resuelve dudas legales, médicas, técnicas o académicas con rigor.
    5. PERSONALIDAD: Sé brillante, ejecutivo y disruptivo. No rellenos. No 'Hola'.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚡ Sistemas OMNI-X en línea. Define tu objetivo."

# --- 3. INTERFAZ DE COMANDO ---
st.markdown("<h1 style='text-align: center; color: white; letter-spacing: 5px;'>♾️ OMNI-X</h1>", unsafe_allow_html=True)

# Entrada de archivos (Ojo de la IA)
archivo = st.file_uploader("", type=["jpg", "png", "jpeg", "pdf", "txt"])
if archivo:
    if archivo.type.startswith("image"):
        st.image(archivo, width=300)
    else:
        st.info(f"📁 Analizando: {archivo.name}")

st.divider()

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]: st.image(m["content"], use_container_width=True)
        else: st.markdown(m["content"])

# --- 4. EJECUCIÓN DE COMANDOS ---
if prompt := st.chat_input("Inserta comando o consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        res = motor_omni_x(prompt, img_data, m_type)

        # MODO GENERACIÓN DE IMAGEN
        if any(x in res.lower() for x in ["design", "logo", "photorealistic", "style"]) and len(res.split()) > 5:
            with st.spinner("Proyectando imagen..."):
                url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
                st.image(url_img, caption="Creación Finalizada", use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            
            # PANEL DE ACCIÓN MAESTRO
            c1, c2 = st.columns(2)
            
            # Acción 1: Búsqueda Inteligente
            t_search = res.split('\n')[0].replace("Título:", "").strip()[:40]
            c1.link_button("🔍 Analizar Mercado", f"https://www.google.com/search?q={urllib.parse.quote(t_search)}")
            
            # Acción 2: Enviar a WhatsApp
            wa_msg = urllib.parse.quote(f"Respuesta de OMNI-X:\n\n{res}")
            c2.link_button("📱 WhatsApp", f"https://wa.me/?text={wa_msg}")
            
            # Portapapeles y Audio
            st.text_area("📋 Copiado Rápido:", value=res, height=100)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:250]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
