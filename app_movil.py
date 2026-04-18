import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def hablar_con_gemini(mensaje):
    # Probamos el modelo Pro, que es el más estable para claves nuevas
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": mensaje}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            # Esto nos dirá el error REAL de Google
            datos_error = r.json()
            msg = datos_error.get('error', {}).get('message', 'Error desconocido')
            return f"🚫 Google dice: {msg}. (Código: {r.status_code})"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.title("🌌 CREAL OMNI-INTELLIGENCE")

with st.sidebar:
    st.title("🛡️ Nodo Central")
    nombre = st.text_input("Tu nombre", "Creal")
    tele_id = st.text_input("ID Telegram", "8449303559")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe 'Estás ahí?'..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Responde brevemente a {nombre}: {p}")
        st.markdown(res)
        
        # Botón de audio solo si no hay error
        if "🚫" not in res and "❌" not in res:
            if st.button("🔊 Enviar Audio"):
                tts = gTTS(text=res[:250], lang='es')
                tts.save("voice.mp3")
                token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})

    st.session_state.messages.append({"role": "assistant", "content": res})
