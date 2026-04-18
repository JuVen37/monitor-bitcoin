import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def hablar_con_gemini(mensaje):
    # Probamos los dos modelos principales por si uno está bloqueado
    modelos = ["gemini-1.5-flash", "gemini-pro"]
    
    for mod in modelos:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": mensaje}]}]}
        headers = {'Content-Type': 'application/json'}
        
        try:
            r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            if r.status_code == 200:
                return r.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    return "⏳ La clave sigue en proceso de activación. Por favor, pulsa 'Rerun' en el menú de arriba en 2 minutos."

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

if p := st.chat_input("Escribe 'Hola' para probar..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Eres la IA de Creal. Responde a {nombre}: {p}")
        st.markdown(res)
        
        if "⏳" not in res: # Solo muestra el botón si la IA respondió de verdad
            if st.button("🔊 Enviar Audio"):
                tts = gTTS(text=res[:250], lang='es')
                tts.save("voice.mp3")
                token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
                st.success("Audio enviado")

    st.session_state.messages.append({"role": "assistant", "content": res})
