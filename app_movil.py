import streamlit as st
import google.generativeai as genai
import requests
from gtts import gTTS

# --- CONFIGURACIÓN ---
GOOGLE_API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

# Configuración forzada
genai.configure(api_key=GOOGLE_API_KEY)

def obtener_modelo():
    # Intentamos el nombre más moderno y estable
    try:
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return genai.GenerativeModel('gemini-pro')

model = obtener_modelo()

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

if p := st.chat_input("Escribe 'Hola' para probar..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Respuesta directa
            response = model.generate_content(p)
            res = response.text
        except Exception as e:
            res = f"⚠️ Sigue habiendo un bloqueo. Por favor, haz el paso de 'Delete App' en Streamlit. Error: {str(e)}"
        
        st.markdown(res)
        
        if st.button("🔊 Audio"):
            tts = gTTS(text=res[:200], lang='es')
            tts.save("voice.mp3")
            token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
            requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})

    st.session_state.messages.append({"role": "assistant", "content": res})
