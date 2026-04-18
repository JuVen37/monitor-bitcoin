import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN SEGURA ---
# Ahora leemos AMBAS claves desde la caja fuerte (Secrets)
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

# Ya sabemos que este es tu ID real, déjalo así
nombre = st.sidebar.text_input("Tu Nombre", "Creal")
tele_id = st.sidebar.text_input("ID Telegram", "8449303559")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe algo y pide el audio..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Responde a {nombre}: {p}")
        st.markdown(res)
        
        if "🚫" not in res and "❌" not in res:
            if st.button("🔊 Enviar Audio a Telegram"):
                try:
                    tts = gTTS(text=res[:250], lang='es')
                    tts.save("voice.mp3")
                    # Usamos el token escondido
                    tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendAudio?chat_id={tele_id}"
                    
                    with open("voice.mp3", "rb") as audio_file:
                        r_tg = requests.post(tg_url, files={'audio': audio_file})
                    
                    if r_tg.status_code == 200:
                        st.success("✅ ¡Audio enviado con éxito a tu móvil!")
                    else:
                        st.error(f"❌ Error de Telegram: {r_tg.text}")
                except Exception as e:
                    st.error(f"❌ Error interno de audio: {str(e)}")

    st.session_state.messages.append({"role": "assistant", "content": res})
