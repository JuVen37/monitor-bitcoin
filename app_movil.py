import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ No se encuentra la clave en Misterios.")
    st.stop()

def hablar_con_gemini(mensaje):
    # Usamos v1beta y el nombre completo del modelo que Google exige ahora
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
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
            # Si el flash falla, intentamos el gemini-pro que es el más viejo y estable
            url_backup = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
            r_backup = requests.post(url_backup, headers=headers, data=json.dumps(payload))
            if r_backup.status_code == 200:
                return r_backup.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"🚫 Error persistente. Google dice: {r.status_code}"
    except:
        return "❌ Error de conexión."

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.title("🌌 CREAL OMNI-AI")

nombre = st.sidebar.text_input("Nombre", "Creal")
tele_id = st.sidebar.text_input("ID Telegram", "8449303559")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe 'Hola' para despertar a la IA..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Responde a {nombre}: {p}")
        st.markdown(res)
        
        if "🚫" not in res and "❌" not in res:
            if st.button("🔊 Enviar Audio"):
                tts = gTTS(text=res[:250], lang='es')
                tts.save("voice.mp3")
                token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
                st.success("¡Audio enviado!")

    st.session_state.messages.append({"role": "assistant", "content": res})
