import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. DISEÑO CINEMATOGRÁFICO ---
st.set_page_config(page_title="CREAL OMNI: ULTIMATUM", page_icon="🦾", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #050505; }
    .stChatMessage { border-radius: 20px; background-color: #111; border: 1px solid #4A90E2; }
    /* Botones Neón */
    .stButton>button { 
        background: linear-gradient(45deg, #4A90E2, #00ffcc); 
        color: black; font-weight: bold; border-radius: 10px; border: none;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. CEREBRO DE ALTA PRECISIÓN ---
def llamar_ia_ultimatum(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = """
    Eres CREAL OMNI ULTIMATUM. Tu objetivo es el éxito financiero del usuario.
    PROTOCOLOS:
    - ANALISTA VINTED: Si ves ropa, da Título, Descripción y Tasación.
    - MODO INTERNACIONAL: Genera siempre un resumen corto de la descripción en Francés e Italiano para maximizar ventas.
    - BUSCADOR: Extrae el nombre exacto del producto para búsqueda externa.
    - DISEÑO: Si piden imagen, genera el prompt detallado en inglés.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión Segura Establecida."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🦾 OMNI ULTIMATUM</h1>", unsafe_allow_html=True)

archivo = st.file_uploader("", type=["jpg", "png", "jpeg"])
if archivo:
    st.image(archivo, width=250)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🦾" if m["role"] == "assistant" else "👤"):
        if "https://image" in m["content"]: st.image(m["content"])
        else: st.markdown(m["content"])

if prompt := st.chat_input("Comando de ejecución..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="🦾"):
        img_data, m_type = None, None
        if archivo:
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        res = llamar_ia_ultimatum(prompt, img_data, m_type)

        # MODO DISEÑO
        if any(x in res.lower() for x in ["design", "logo", "style"]) and len(res.split()) > 5:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Resultado Visual")
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            
            # --- NUEVAS HERRAMIENTAS DE PODER ---
            col1, col2 = st.columns(2)
            
            # Botón Espía: Busca el producto en Vinted
            nombre_producto = res.split('\n')[0].replace("Título:", "").strip()
            url_vinted = f"https://www.vinted.es/vetements?search_text={urllib.parse.quote(nombre_producto)}"
            col1.link_button("🔍 Ver competencia", url_vinted)
            
            # Botón WhatsApp: Envía el anuncio rápido
            msg_whatsapp = urllib.parse.quote(f"Mira este anuncio que he creado con CREAL OMNI:\n\n{res}")
            col2.link_button("📱 Enviar por WhatsApp", f"https://wa.me/?text={msg_whatsapp}")

            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Area de copiado y Audio
            st.text_area("📋 Texto Final:", value=res, height=100)
            try:
                texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:200]
                tts = gTTS(text=texto_voz, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
