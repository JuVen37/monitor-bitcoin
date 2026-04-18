import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse

# --- 1. CONFIGURACIÓN DE "MODO APP" ---
st.set_page_config(page_title="CREAL OMNI", page_icon="💎", layout="centered")

# Este bloque de abajo engaña al móvil para que se vea como una App real
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    </head>
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #080808; }
    .stChatMessage { border-radius: 25px; background-color: #121212; border: 1px solid #1f2937; }
    /* Ajuste para que no se mueva el chat en el móvil */
    .main .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. MOTOR OMNI APEX ---
def llamar_ia_apex(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    instrucciones = "Eres CREAL OMNI APEX. Eres un socio de negocios de élite. Si ves ropa, analízala para Vinted con títulos SEO, descripciones potentes y precio de mercado."
    
    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión establecida. Proyecta tu visión."

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2; font-size: 28px;'>💎 CREAL OMNI</h1>", unsafe_allow_html=True)

foto = st.file_uploader("📸 ESCANEAR", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, width=250)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "💎" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        if "https://image" in m["content"]: st.image(m["content"])
        else: st.markdown(m["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="💎"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        res = llamar_ia_apex(prompt, img_data, m_type)

        if any(x in res.lower() for x in ["design", "logo", "style"]) and len(res.split()) > 5:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Generado")
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            
            # BOTONES DE ACCIÓN
            c1, c2 = st.columns(2)
            t_clean = res.split('\n')[0].replace("Título:", "").strip()[:30]
            c1.link_button("🔍 Ver Mercado", f"https://www.vinted.es/vetements?search_text={urllib.parse.quote(t_clean)}")
            c2.link_button("📱 WhatsApp", f"https://wa.me/?text={urllib.parse.quote(res)}")
            
            st.text_area("📋 Copiar:", value=res, height=100)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:250]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
