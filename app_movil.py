import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse

# --- 1. DISEÑO UNIVERSAL PREMIUM ---
st.set_page_config(page_title="CREAL OMNI", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #000000; }
    .stChatMessage { border-radius: 20px; background-color: #111; border: 1px solid #222; margin-bottom: 15px; }
    .stFileUploader section { background-color: #0d1117 !important; border: 1px solid #4A90E2 !important; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. CEREBRO MULTIDIMENSIONAL ---
def llamar_ia_total(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    # Instrucciones maestras para ser un experto en TODO
    instrucciones = """
    Eres CREAL OMNI, una inteligencia superior diseñada para resolver CUALQUIER problema.
    
    ACTÚA SEGÚN EL CONTEXTO:
    - SI ES ROPA/PRODUCTO: Crea el mejor anuncio para venderlo (título, descripción, precio).
    - SI ES UN TEXTO/DOCUMENTO: Analízalo, resúmelo y destaca lo importante.
    - SI ES UN OBJETO COTIDIANO: Explica qué es, cómo funciona o para qué sirve.
    - SI ES CÓDIGO/MATES: Resuelve el problema paso a paso.
    - SI PIDEN IMAGEN/LOGO: Genera un prompt profesional en inglés para diseño.
    
    Sé directo, brillante y usa un lenguaje que haga ganar tiempo y dinero al usuario.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ Error de conexión. El sistema está saturado o sin red."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>💎 CREAL OMNI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Inteligencia Visual y Textual Ilimitada</p>", unsafe_allow_html=True)

# Cargador universal
archivo = st.file_uploader("📸 SUBIR IMAGEN O DOCUMENTO", type=["jpg", "png", "jpeg", "pdf", "txt"])
if archivo:
    if archivo.type.startswith("image"):
        st.image(archivo, width=300)
    else:
        st.info(f"📁 Documento cargado: {archivo.name}")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "💎" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]:
            st.image(m["content"])
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Pregúntame lo que sea o analiza un archivo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💎"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        res = llamar_ia_total(prompt, img_data, m_type)
        
        # Lógica de imagen
        if any(x in res.lower() for x in ["design", "logo", "image", "photorealistic"]) and len(res.split()) > 5:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Resultado Visual")
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Botones inteligentes (solo aparecen si son útiles)
            col1, col2 = st.columns(2)
            # WhatsApp siempre es útil
            wa_text = urllib.parse.quote(f"Mira lo que me ha dicho CREAL OMNI:\n\n{res[:500]}")
            col1.link_button("📱 Compartir en WhatsApp", f"https://wa.me/?text={wa_text}")
            
            # Audio
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:200]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
