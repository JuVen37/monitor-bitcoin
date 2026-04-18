import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re

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

# Quitamos el ID de Telegram porque ya no hace falta
nombre = st.sidebar.text_input("¿Cómo te llamas?", "Usuario")
st.sidebar.markdown("---")
st.sidebar.info("💡 Escribe un mensaje y la IA generará texto y audio directamente aquí.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujamos el historial
for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

# Caja de chat principal
if p := st.chat_input("Pregúntale algo a Creal..."):
    # 1. Mostramos lo que pregunta el usuario
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): 
        st.markdown(p)

    # 2. Mostramos la respuesta de la IA y su reproductor de audio
    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Responde a {nombre}: {p}")
        st.markdown(res)
        
        if "🚫" not in res and "❌" not in res:
            with st.spinner("Generando voz..."):
                try:
                    # Limpiamos el texto y generamos el audio en la RAM
                    texto_limpio = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)
                    if len(texto_limpio.strip()) > 0:
                        tts = gTTS(text=texto_limpio[:250], lang='es')
                        archivo_en_ram = io.BytesIO()
                        tts.write_to_fp(archivo_en_ram)
                        archivo_en_ram.seek(0)
                        
                        # REPRODUCTOR INTEGRADO: Aparece justo debajo del texto
                        st.audio(archivo_en_ram, format="audio/mp3")
                except Exception as e:
                    st.error("No se pudo generar el audio para este mensaje.")

    # Guardamos la respuesta en el historial
    st.session_state.messages.append({"role": "assistant", "content": res})
