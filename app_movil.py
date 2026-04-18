import streamlit as st
import google.generativeai as genai
import requests
from gtts import gTTS
import os

# --- 1. CONFIGURACIÓN DEL CEREBRO ---
GOOGLE_API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def cargar_modelo():
    genai.configure(api_key=GOOGLE_API_KEY)
    # Lista de nombres posibles que usa Google según la región
    nombres_modelo = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for nombre in nombres_modelo:
        try:
            m = genai.GenerativeModel(nombre)
            # Prueba rápida para ver si el modelo responde
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = cargar_modelo()

# --- 2. APARIENCIA PREMIUM ---
st.set_page_config(page_title="CREAL OMNI-AI", page_icon="🌌", layout="wide")
st.markdown("<style>.main { background: #000; color: #00ffc8; }</style>", unsafe_allow_html=True)

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ Nodo Central")
    user_name = st.text_input("¿Quién eres?", "Creal")
    tele_id = st.text_input("ID Telegram", "8449303559")
    st.info(f"Usuario activo: {user_name}")

# --- 4. CHAT MAESTRO ---
st.title("🌌 CREAL OMNI-INTELLIGENCE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Pregúntame lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        try:
            if model is None:
                res = "⚠️ Google no ha autorizado ningún modelo para esta clave aún. Espera 5 min y reinicia."
            else:
                ctx = f"Eres la IA de Creal. Usuario: {user_name}. Sé breve y brillante."
                response = model.generate_content(f"{ctx}\nPregunta: {p}")
                res = response.text
        except Exception as e:
            res = f"⚠️ Error final: {str(e)}. Prueba a pulsar 'Reboot App' en Streamlit."
        
        st.markdown(res)
        
        if st.button("🔊 Enviar audio"):
            tts = gTTS(text=res[:200], lang='es')
            tts.save("voice.mp3")
            token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
            requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
            st.success("✅ Audio enviado")

    st.session_state.messages.append({"role": "assistant", "content": res})
