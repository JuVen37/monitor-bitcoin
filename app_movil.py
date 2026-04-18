import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN SEGURA ---
if "GOOGLE_API_KEY" in st.secrets:
    # Quitamos los espacios invisibles por si acaso
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
else:
    st.error("⚠️ No se encuentra la clave en Misterios.")
    st.stop()

def hablar_con_gemini(mensaje):
    # 🎯 EL CAMBIO MÁGICO: Usamos el modelo exacto de tu lista
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": mensaje}]
        }]
    }
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
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("¡Despierta, Creal!"):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Eres la IA del sistema Creal. Responde amablemente a {nombre}: {p}")
        st.markdown(res)
        
        if "🚫" not in res and "❌" not in res:
            if st.button("🔊 Enviar Audio a Telegram"):
                try:
                    tts = gTTS(text=res[:250], lang='es')
                    tts.save("voice.mp3")
                    token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                    requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
                    st.success("✅ ¡Audio enviado con éxito!")
                except:
                    st.error("Error al enviar el audio.")

    st.session_state.messages.append({"role": "assistant", "content": res})
