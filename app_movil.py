import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"
# CAMBIO CLAVE: Usamos versión v1 (estable) y modelo gemini-pro
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def hablar_con_gemini(mensaje):
    # Estructura de datos exacta para la versión estable
    payload = {
        "contents": [{
            "parts": [{"text": mensaje}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ Error de Google ({response.status_code}): {response.json()['error']['message']}"
    except Exception as e:
        return f"⚠️ Error de conexión: {str(e)}"

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.markdown("<style>.main { background: #000; color: #00ffc8; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ Nodo Central")
    nombre = st.text_input("Nombre", "Creal")
    tele_id = st.text_input("ID Telegram", "8449303559")

st.title("🌌 CREAL OMNI-INTELLIGENCE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe 'Hola' para probar la conexión estable..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Eres la IA de Creal. Responde a {nombre}: {p}")
        st.markdown(res)
        
        if st.button("🔊 Audio"):
            try:
                tts = gTTS(text=res[:200], lang='es')
                tts.save("voice.mp3")
                token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
            except:
                st.error("Error al generar audio.")

    st.session_state.messages.append({"role": "assistant", "content": res})
