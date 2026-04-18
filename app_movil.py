import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
# Esta es tu clave que ya sabemos que es la buena
API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def hablar_con_gemini(mensaje):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": mensaje}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {r.status_code}. Google dice: {r.text}"
    except:
        return "Error de conexión."

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.title("🌌 CREAL OMNI-AI")

nombre = st.sidebar.text_input("Tu nombre", "Creal")
tele_id = st.sidebar.text_input("ID Telegram", "8449303559")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe algo aquí..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Eres la IA de Creal. Responde a {nombre}: {p}")
        st.markdown(res)
        
        if st.button("🔊 Enviar Audio"):
            try:
                tts = gTTS(text=res[:200], lang='es')
                tts.save("voice.mp3")
                token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
                st.success("¡Audio enviado!")
            except:
                st.error("Error con el audio.")

    st.session_state.messages.append({"role": "assistant", "content": res})
