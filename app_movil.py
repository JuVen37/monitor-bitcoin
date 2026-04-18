import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. INTERFAZ ULTRA-PREMIUM (ESTILO CYBERPUNK/DARK) ---
st.set_page_config(page_title="CREAL OMNI: GENESIS", page_icon="🔱", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: radial-gradient(circle at center, #111 0%, #000 100%); }
    .stChatMessage { border-radius: 20px; background-color: #161b22; border: 1px solid #30363d; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    
    /* Personalización de inputs */
    .stChatInputContainer { padding-bottom: 20px; }
    .stFileUploader section { background-color: #0d1117 !important; border: 1px solid #4A90E2 !important; }
    
    /* Botones de Acción Especial */
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2 0%, #63b3ed 100%);
        color: white; border-radius: 12px; border: none; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. CEREBRO TOTAL: GÉNESIS ---
def llamar_ia_genesis(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = """
    Eres CREAL OMNI GÉNESIS. Tu misión es la excelencia absoluta.
    
    MODOS DE OPERACIÓN:
    1. EXPERTO VINTED: Si ves ropa, genera: Título SEO, Descripción en Español, Francés e Italiano, y Tasación.
    2. ASISTENTE DE LUJO: Sé elegante, breve y resuelve dudas complejas.
    3. DETECTOR DE ETIQUETAS: Si ves una etiqueta, identifica marca, composición y cuidados.
    4. DISEÑADOR: Si piden logos o imágenes, genera el prompt detallado en inglés.
    
    ESTILO: Sin introducciones robóticas. Directo al grano con emojis de alta gama.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión segura establecida. Ejecuta tu comando."

# --- 3. INTERFAZ DE USUARIO ---
st.markdown("<h1 style='text-align: center; color: #4A90E2; letter-spacing: 2px;'>🔱 OMNI GÉNESIS</h1>", unsafe_allow_html=True)

# Sección de Carga
with st.container():
    foto = st.file_uploader("📸 ESCANEAR PRENDA / DOCUMENTO", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, width=300, caption="Elemento cargado en el sistema")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar historial
for m in st.session_state.messages:
    avatar = "🔱" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]: st.image(m["content"])
        else: st.markdown(m["content"])

# Procesamiento de Comandos
if prompt := st.chat_input("¿Qué misión ejecutamos?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="🔱"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        res = llamar_ia_genesis(prompt, img_data, m_type)

        # LÓGICA DE IMAGEN (DISEÑADOR)
        if any(x in res.lower() for x in ["design", "logo", "photorealistic", "illustration"]) and len(res.split()) > 5:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Proyección Generada")
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            
            # --- PANEL DE ACCIÓN RÁPIDA ---
            st.markdown("### ⚡ Herramientas de Ejecución")
            c1, c2, c3 = st.columns(3)
            
            # 1. Búsqueda de competencia
            t_prod = res.split('\n')[0].replace("Título:", "").strip()[:30]
            url_v = f"https://www.vinted.es/vetements?search_text={urllib.parse.quote(t_prod)}"
            c1.link_button("🔍 Competencia", url_v)
            
            # 2. Compartir WhatsApp
            wa_text = urllib.parse.quote(f"Generado con OMNI GÉNESIS:\n\n{res}")
            c2.link_button("📱 WhatsApp", f"https://wa.me/?text={wa_text}")
            
            # 3. Traducir (Modo rápido)
            c3.button("🌍 Modo Internacional", on_click=lambda: st.toast("Traducciones incluidas en el texto!"))

            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Copiado y Audio
            st.text_area("📋 Portapapeles:", value=res, height=120)
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:250]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
