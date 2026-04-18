import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re

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

for m in st.session_state.messages:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    ultimo_mensaje = st.session_state.messages[-1]["content"]
    
    if "🚫" not in ultimo_mensaje and "❌" not in ultimo_mensaje:
        if st.button("🔊 Enviar Audio a Telegram"):
            with st.spinner("Creando audio en memoria RAM..."):
                try:
                    # 1. Limpieza de símbolos
                    texto_limpio = re.sub(r'[^\w\s.,;:!?¿¡]', '', ultimo_mensaje)
                    if len(texto_limpio.strip()) == 0:
                        texto_limpio = "Error. Mensaje vacío."
                    
                    # 2. Generamos el audio en la RAM (¡Sin guardarlo en disco!)
                    tts = gTTS(text=texto_limpio[:250], lang='es')
                    archivo_en_ram = io.BytesIO()
                    tts.write_to_fp(archivo_en_ram)
                    
                    # 3. Probamos en la web (Rebobinamos el archivo para leerlo)
                    archivo_en_ram.seek(0)
                    st.audio(archivo_en_ram, format="audio/mp3")
                    
                    # 4. Enviamos a Telegram
                    archivo_en_ram.seek(0) # Volvemos a rebobinar
                    tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendAudio?chat_id={tele_id}"
                    
                    # Le decimos a Telegram que el archivo se llama "voice.mp3" aunque esté flotando en la memoria
                    archivos = {'audio': ('voice.mp3', archivo_en_ram, 'audio/mp3')}
                    r_tg = requests.post(tg_url, files=archivos, timeout=15)
                    
                    if r_tg.status_code == 200:
                        st.success("✅ ¡Audio creado en RAM y enviado a Telegram!")
                    else:
                        st.error(f"❌ Error de Telegram: {r_tg.text}")

                except Exception as e:
                    st.error(f"❌ Error interno: {str(e)}")

if p := st.chat_input("Escribe algo..."):
    st.session_state.messages.append({"role": "user", "content": p})
    res = hablar_con_gemini(f"Responde a {nombre}: {p}")
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.rerun()
