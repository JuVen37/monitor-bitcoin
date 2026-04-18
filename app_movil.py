import streamlit as st
import requests
import json
from gtts import gTTS

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

# Dibujamos el historial de mensajes
for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

# Si el ÚLTIMO mensaje es de la IA, mostramos el botón de forma fija
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    ultimo_mensaje = st.session_state.messages[-1]["content"]
    
    if "🚫" not in ultimo_mensaje and "❌" not in ultimo_mensaje:
        # El botón ahora está "suelto", no desaparecerá al pulsarlo
        if st.button("🔊 Enviar Última Respuesta por Audio"):
            with st.spinner("Creando y enviando audio..."):
                try:
                    tts = gTTS(text=ultimo_mensaje[:250], lang='es')
                    tts.save("voice.mp3")
                    
                    tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendAudio?chat_id={tele_id}"
                    with open("voice.mp3", "rb") as audio_file:
                        r_tg = requests.post(tg_url, files={'audio': audio_file})
                    
                    if r_tg.status_code == 200:
                        st.success("✅ ¡Audio enviado con éxito a tu Telegram!")
                    else:
                        st.error(f"❌ Error de Telegram: {r_tg.text}")
                except Exception as e:
                    st.error(f"❌ Error interno de audio: {str(e)}")

# Caja de chat (Cuando escribes, recarga la página para que salga arriba)
if p := st.chat_input("Escribe algo a Creal..."):
    # Guardamos tu mensaje
    st.session_state.messages.append({"role": "user", "content": p})
    
    # Obtenemos y guardamos la respuesta
    res = hablar_con_gemini(f"Responde a {nombre}: {p}")
    st.session_state.messages.append({"role": "assistant", "content": res})
    
    # Recargamos la app para que aparezca el mensaje y el botón
    st.rerun()
