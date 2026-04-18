import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. CONFIGURACIÓN SEGURA ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
else:
    st.error("⚠️ Faltan las claves en la sección de Misterios de Streamlit.")
    st.stop()

def hablar_con_gemini(mensaje):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": mensaje}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚫 Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Error de red: {str(e)}"

# --- 2. INTERFAZ ESTILO CHATGPT ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.title("🌌 CREAL OMNI")
st.caption("Asistente de IA Público")

nombre = st.sidebar.text_input("¿Cómo te llamas?", "Usuario")
st.sidebar.markdown("---")
st.sidebar.info("💡 Escribe un mensaje y la IA generará texto y audio directamente aquí.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

if p := st.chat_input("Pregúntale algo a Creal..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): 
        st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Responde a {nombre}: {p}")
        st.markdown(res)
        
        if "🚫" not in res and "❌" not in res:
            with st.spinner("Generando voz para móviles..."):
                try:
                    # Limpiamos el texto
                    texto_limpio = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)
                    if len(texto_limpio.strip()) > 0:
                        # Generamos audio en RAM
                        tts = gTTS(text=texto_limpio[:250], lang='es')
                        archivo_en_ram = io.BytesIO()
                        tts.write_to_fp(archivo_en_ram)
                        archivo_en_ram.seek(0)
                        
                        # 🎯 EL TRUCO INFALIBLE: Convertimos el audio a texto Base64
                        base64_audio = base64.b64encode(archivo_en_ram.read()).decode("utf-8")
                        
                        # Creamos un reproductor HTML nativo
                        audio_html = f'<audio controls><source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3"></audio>'
                        
                        # Lo mostramos en la pantalla
                        st.markdown(audio_html, unsafe_allow_html=True)
                        
                except Exception as e:
                    # Ahora si falla, te dirá el motivo exacto en rojo
                    st.error(f"❌ Error interno al generar audio: {str(e)}")

    st.session_state.messages.append({"role": "assistant", "content": res})
