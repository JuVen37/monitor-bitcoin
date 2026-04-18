import streamlit as st
import requests
import json
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def obtener_modelo_valido():
    # Paso A: Listar todos los modelos disponibles para tu clave
    url_list = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
    try:
        r = requests.get(url_list)
        if r.status_code == 200:
            modelos = r.json().get('models', [])
            # Buscamos uno que permita generar contenido (pueden ser flash o pro)
            for m in modelos:
                if "generateContent" in m.get('supportedGenerationMethods', []):
                    return m['name'] # Retorna algo como 'models/gemini-1.5-flash-latest'
        return None
    except:
        return None

def hablar_con_gemini(mensaje):
    nombre_modelo = obtener_modelo_valido()
    if not nombre_modelo:
        return "❌ No se encontraron modelos disponibles para esta clave. Revisa Google AI Studio."
    
    # Paso B: Usar el modelo encontrado con la versión correcta
    url = f"https://generativelanguage.googleapis.com/v1/{nombre_modelo}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": mensaje}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚫 Error {r.status_code}: {r.json().get('error', {}).get('message')}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.title("🌌 CREAL OMNI-AUTO-SCAN")

with st.sidebar:
    st.title("🛡️ Nodo Central")
    nombre = st.text_input("Tu nombre", "Creal")
    tele_id = st.text_input("ID Telegram", "8449303559")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe 'Hola' para escanear..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        res = hablar_con_gemini(f"Responde a {nombre}: {p}")
        st.markdown(res)
        
        if "❌" not in res and "🚫" not in res:
            if st.button("🔊 Enviar Audio"):
                tts = gTTS(text=res[:250], lang='es')
                tts.save("voice.mp3")
                token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})

    st.session_state.messages.append({"role": "assistant", "content": res})
