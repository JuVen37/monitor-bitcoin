import streamlit as st
import requests
import json
import os
import re
import time

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

def generar_audio_antibloqueo(texto):
    # Limpiamos asteriscos y símbolos
    texto_limpio = re.sub(r'[^\w\s.,;:!?¿¡]', '', texto)
    if len(texto_limpio.strip()) == 0:
        texto_limpio = "Error. Mensaje vacío."
        
    # Usamos una API pública para saltarnos el bloqueo de Google/Streamlit
    url_api = "https://api.soundoftext.com/engine"
    # Esta API gratuita permite hasta 200 caracteres por audio
    payload = {"text": texto_limpio[:200], "voice": "es-ES"}
    
    try:
        # 1. Pedimos que fabrique el MP3
        req = requests.post(url_api, json=payload)
        if req.status_code == 200:
            audio_id = req.json().get("id")
            time.sleep(1.5) # Damos 1.5 segundos para que lo procese
            
            # 2. Descargamos el MP3 REAL
            url_descarga = f"https://api.soundoftext.com/sounds/{audio_id}"
            mp3_data = requests.get(url_descarga)
            
            if mp3_data.status_code == 200:
                with open("voice.mp3", "wb") as f:
                    f.write(mp3_data.content)
                return True
    except:
        pass
    return False

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
    ultimo_mensaje = st.session_state.messages[-1]["content"]
    
    if "🚫" not in ultimo_mensaje and "❌" not in ultimo_mensaje:
        if st.button("🔊 Enviar Audio a Telegram"):
            with st.spinner("Conectando con el nuevo motor de voz..."):
                exito = generar_audio_antibloqueo(ultimo_mensaje)
                
                if exito:
                    # ENVIAMOS A TELEGRAM DIRECTAMENTE
                    tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendAudio?chat_id={tele_id}"
                    try:
                        with open("voice.mp3", "rb") as f:
                            r_tg = requests.post(tg_url, files={'audio': f})
                        
                        if r_tg.status_code == 200:
                            st.success("✅ ¡Audio REAL generado y enviado!")
                            # Ponemos el reproductor en la web también para que lo veas
                            st.audio("voice.mp3", format="audio/mp3") 
                        else:
                            st.error(f"❌ Error de Telegram: {r_tg.text}")
                    except Exception as e:
                        st.error(f"❌ Error interno al enviar: {str(e)}")
                else:
                    st.error("❌ Falló el servidor de voz. Inténtalo de nuevo en unos segundos.")

if p := st.chat_input("Escribe algo..."):
    st.session_state.messages.append({"role": "user", "content": p})
    res = hablar_con_gemini(f"Responde a {nombre}: {p}")
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.rerun()
