import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse
from datetime import datetime

# --- 1. DISEÑO APEX (MÁXIMA ELEGANCIA) ---
st.set_page_config(page_title="CREAL OMNI: APEX", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #080808; }
    .stChatMessage { border-radius: 25px; background-color: #121212; border: 1px solid #1f2937; }
    .stChatInputContainer { padding-bottom: 30px; }
    /* Estilo del Sidebar Premium */
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #4A90E2; }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. PANEL DE CONFIGURACIÓN DE NEGOCIO (EL "CEREBRO" DEL USUARIO) ---
with st.sidebar:
    st.title("💎 Perfil APEX")
    user_role = st.selectbox("Especialidad:", ["Vendedor Vinted/Moda", "Consultor de Negocios", "Diseñador Creativo", "Analista de Datos"])
    target_tone = st.radio("Tono de la IA:", ["💎 Lujo/Elegante", "🔥 Hype/Agresivo", "🧠 Profesional/Directo"])
    st.divider()
    st.info("OMNI APEX ahora adapta su lenguaje a tu perfil seleccionado.")

# --- 3. MOTOR OMNI APEX ---
def llamar_ia_apex(mensaje, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    instrucciones = f"""
    Eres CREAL OMNI APEX. Estás configurado para un usuario que es: {user_role}.
    Tu tono actual es: {target_tone}.
    
    CAPACIDADES EXCLUSIVAS:
    - MODO VENTA: Si ves ropa, analiza tendencia actual 2024-2026. Da el precio 'Gana-Dinero' y el 'Precio-Hype'.
    - LINGÜÍSTICA: Si el tono es Lujo, usa palabras sofisticadas. Si es Hype, usa emojis y frases de urgencia.
    - DISEÑO: Genera prompts visuales de nivel estudio fotográfico.
    - REGLA: No menciones que eres una IA. Eres un socio de negocios.
    """

    partes = [{"text": instrucciones}, {"text": mensaje}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Conexión APEX establecida. Proyecta tu visión."

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #4A90E2; font-weight: 800;'>💎 OMNI APEX</h1>", unsafe_allow_html=True)

# Cargador Central
foto = st.file_uploader("", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, width=300, caption="Elemento en análisis")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="💎" if m["role"] == "assistant" else "👤"):
        if "https://image" in m["content"]: st.image(m["content"])
        else: st.markdown(m["content"])

if prompt := st.chat_input("Ejecutar comando maestro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="💎"):
        img_data, m_type = None, None
        if foto:
            img_data = base64.b64encode(foto.getvalue()).decode("utf-8")
            m_type = foto.type
            
        res = llamar_ia_apex(prompt, img_data, m_type)

        if any(x in res.lower() for x in ["design", "logo", "photorealistic"]) and len(res.split()) > 5:
            url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(res)}"
            st.image(url_img, caption="Generación Finalizada")
            st.session_state.messages.append({"role": "assistant", "content": url_img})
        else:
            st.markdown(res)
            
            # --- TOOLBOX DE ACCIÓN ---
            c1, c2, c3 = st.columns(3)
            # Extraer título para búsqueda
            t_clean = res.split('\n')[0].replace("Título:", "").strip()[:30]
            c1.link_button("🔍 Ver Mercado", f"https://www.vinted.es/vetements?search_text={urllib.parse.quote(t_clean)}")
            c2.link_button("📱 WhatsApp", f"https://wa.me/?text={urllib.parse.quote(res)}")
            
            # Botón de Copiado Rápido
            st.text_area("📋 Portapapeles Inteligente:", value=res, height=120)

            st.session_state.messages.append({"role": "assistant", "content": res})
            
            # Audio Neural
            try:
                texto_v = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)[:250]
                tts = gTTS(text=texto_v, lang='es')
                b = io.BytesIO(); tts.write_to_fp(b); b64 = base64.b64encode(b.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass
