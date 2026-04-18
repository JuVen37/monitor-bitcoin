import streamlit as st
import requests
import json
from gtts import gTTS
import os

# --- 1. CONFIGURACIÓN SEGURA ---
if "GOOGLE_API_KEY" in st.secrets and "TELEGRAM_TOKEN" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    TG_TOKEN = st.secrets["TELEGRAM_TOKEN"].strip()
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

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.title("🌌 CREAL OMNI-AI")
st.caption("⚡ Conectado a Gemini 2.5 Flash")

nombre = st.sidebar.text_input("Tu Nombre", "Creal")
tele_id = st.sidebar.text_input("ID Telegram", "8449303559")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    if st.button("🔊 Generar y Probar Audio en la Web"):
        with st.spinner("Creando audio..."):
            try:
                # Vamos a forzar una frase corta y perfecta para probar
                texto_prueba = "Hola Juan, esta es una prueba de sonido directa del sistema."
                
                tts = gTTS(text=texto_prueba, lang='es')
                tts.save("voice.mp3")
                
                peso = os.path.getsize("voice.mp3")
                st.info(f"💾 Peso del archivo creado: {peso} bytes")
                
                # REPRODUCTOR WEB INTEGRADO: Pruébalo aquí antes de Telegram
                st.audio("voice.mp3", format="audio/mp3")
                
                # ENVIAR A TELEGRAM AUTOMÁTICAMENTE
                tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendAudio?chat_id={tele_id}"
                with open("voice.mp3", "rb") as f:
                    requests.post(tg_url, files={'audio': f})
                
                st.success("✅ También se ha enviado a Telegram.")

            except Exception as e:
                st.error(f"❌ Error al crear la voz: {str(e)}")

if p := st.chat_input("Escribe algo..."):
    st.session_state.messages.append({"role": "user", "content": p})
    res = hablar_con_gemini(f"Responde a {nombre}: {p}")
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.rerun()
