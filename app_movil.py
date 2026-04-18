import streamlit as st
import google.generativeai as genai
import requests
from gtts import gTTS
import os

# --- 1. CONFIGURACIÓN DEL CEREBRO ---
GOOGLE_API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Intentamos el modelo más moderno, si falla, el sistema nos dirá cuáles hay
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error al conectar con Google AI.")

# --- 2. APARIENCIA PREMIUM ---
st.set_page_config(page_title="CREAL OMNI-AI", page_icon="🌌", layout="wide")
st.markdown("""
    <style>
    .main { background: #000; color: #00ffc8; }
    .stChatFloatingInputContainer { background-color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ Nodo Central")
    user_name = st.text_input("¿Quién eres?", "Creal")
    tele_id = st.text_input("ID Telegram", "8449303559")
    st.divider()
    st.info(f"Usuario activo: {user_name}")

# --- 4. CHAT MAESTRO ---
st.title("🌌 CREAL OMNI-INTELLIGENCE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Hablemos de lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # PROCESO DE RESPUESTA
            ctx = f"Eres la IA de Creal. Usuario: {user_name}. Sé brillante y empático."
            # Generamos la respuesta
            response = model.generate_content(f"{ctx}\nPregunta: {p}")
            res = response.text
        except Exception as e:
            # Si vuelve a dar 404, este mensaje nos dirá exactamente por qué
            res = f"⚠️ Error del sistema: {str(e)}. Intenta reiniciar la app en Streamlit Cloud."
        
        st.markdown(res)
        
        if st.button("🔊 Enviar audio a mi móvil"):
            try:
                tts = gTTS(text=res[:300], lang='es')
                tts.save("voice.mp3")
                token_bot = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
                with open("voice.mp3", "rb") as f:
                    requests.post(f"https://api.telegram.org/bot{token_bot}/sendAudio?chat_id={tele_id}", files={'audio': f})
                st.success("✅ ¡Voz enviada!")
            except:
                st.error("Fallo al generar audio.")

    st.session_state.messages.append({"role": "assistant", "content": res})
